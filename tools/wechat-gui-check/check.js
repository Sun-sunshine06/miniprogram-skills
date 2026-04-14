const fs = require('fs')
const path = require('path')
const childProcess = require('child_process')

const { PNG } = require('pngjs')

const {
  isSevereConsoleEvent,
  pickDataFields,
  resolveDefaultCliPath,
} = require('./lib/check-helpers')
const {
  classifyActionFailure,
  classifyAutomatorProbe,
  classifyCliProbe,
  classifyFatalErrorMessage,
  classifyRunSpecErrorMessage,
  classifyScreenshotWarning,
} = require('./lib/classification')
const { loadAutomator } = require('./lib/load-automator')

const DEFAULT_PROJECT_PATH = path.resolve(__dirname, 'examples', 'fixture-miniapp')
const DEFAULT_OUTPUT_ROOT = path.resolve(DEFAULT_PROJECT_PATH, '.tmp', 'gui-check')
const DEFAULT_CONFIG_PATH = path.resolve(__dirname, 'examples', 'sample.route-config.json')
const DEFAULT_CLI_LAUNCH_TIMEOUT_MS = 15000

function sleep(ms) {
  return new Promise((resolve) => {
    setTimeout(resolve, ms)
  })
}

function withTimeout(label, ms, task) {
  return Promise.race([
    Promise.resolve().then(task),
    new Promise((_, reject) => {
      setTimeout(() => {
        reject(new Error(`${label} timed out after ${ms}ms`))
      }, ms)
    }),
  ])
}

function ensureDir(dirPath) {
  fs.mkdirSync(dirPath, { recursive: true })
}

function readJsonFile(filePath, label = filePath) {
  try {
    return JSON.parse(fs.readFileSync(filePath, 'utf8'))
  } catch (error) {
    throw new Error(`Failed parsing ${label}: ${error && error.message ? error.message : String(error)}`)
  }
}

function timestampSlug() {
  return new Date().toISOString().replace(/[:.]/g, '-')
}

function appendRunTrace(runDir, message) {
  try {
    fs.appendFileSync(path.join(runDir, 'trace.log'), `[${new Date().toISOString()}] ${message}\n`)
  } catch (error) {
    console.warn(`[gui-check] failed writing trace: ${error && error.message ? error.message : String(error)}`)
  }
}

function safeSerialize(value) {
  try {
    return JSON.parse(JSON.stringify(value))
  } catch (error) {
    return String(value)
  }
}

function replaceProjectRootPlaceholders(value, projectPath) {
  if (typeof value !== 'string') {
    return value
  }

  return value.replace(/<project-root>/g, projectPath)
}

function normalizeConfigRoute(route, projectPath) {
  return {
    key: String(route.key || route.route || ''),
    route: String(route.route || ''),
    expectedPath: String(route.expectedPath || '').replace(/^\//, ''),
    primarySelector: String(route.primarySelector || ''),
    titleSelector: String(route.titleSelector || ''),
    settleMs: Number(route.settleMs || 1600),
    dataFields: Array.isArray(route.dataFields) ? route.dataFields.map(String) : [],
    actions: Array.isArray(route.actions) ? route.actions.map((action) => normalizeAction(action)) : [],
    notes: replaceProjectRootPlaceholders(route.notes || '', projectPath),
  }
}

function normalizeAction(action) {
  const normalized = {
    type: String(action.type || ''),
    waitMs: Number(action.waitMs || 0),
    required: action.required !== false,
  }

  if (typeof action.selector === 'string') {
    normalized.selector = action.selector
  }

  if (typeof action.index !== 'undefined') {
    normalized.index = Number(action.index)
  }

  if (action.all === true) {
    normalized.all = true
  }

  if (typeof action.method === 'string') {
    normalized.method = action.method
  }

  if (Object.prototype.hasOwnProperty.call(action, 'payload')) {
    normalized.payload = action.payload
  }

  return normalized
}

function parseArgs(argv) {
  const options = {
    dryRun: false,
    automatorModulePath: process.env.WECHAT_GUI_CHECK_AUTOMATOR_PATH || '',
    cliPath: resolveDefaultCliPath(),
    configPath: DEFAULT_CONFIG_PATH,
    outputRoot: DEFAULT_OUTPUT_ROOT,
    projectPath: DEFAULT_PROJECT_PATH,
    keepOpen: false,
    port: 9420,
    routes: [],
    trustProject: true,
  }

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i]

    if (arg === '--cli-path') {
      options.cliPath = argv[i + 1]
      i += 1
      continue
    }

    if (arg === '--automator-module-path') {
      options.automatorModulePath = argv[i + 1]
      i += 1
      continue
    }

    if (arg === '--config') {
      options.configPath = path.resolve(argv[i + 1])
      i += 1
      continue
    }

    if (arg === '--project-path') {
      options.projectPath = path.resolve(argv[i + 1])
      i += 1
      continue
    }

    if (arg === '--out-dir') {
      options.outputRoot = path.resolve(argv[i + 1])
      i += 1
      continue
    }

    if (arg === '--route') {
      options.routes.push(argv[i + 1])
      i += 1
      continue
    }

    if (arg === '--port') {
      options.port = Number(argv[i + 1])
      i += 1
      continue
    }

    if (arg === '--keep-open') {
      options.keepOpen = true
      continue
    }

    if (arg === '--dry-run') {
      options.dryRun = true
      continue
    }

    if (arg === '--no-trust-project') {
      options.trustProject = false
    }
  }

  return options
}

function loadConfig(configPath, defaultProjectPath, defaultOutputRoot) {
  const rawConfig = readJsonFile(configPath, configPath)
  const projectPath = path.resolve(
    replaceProjectRootPlaceholders(rawConfig.projectPath || defaultProjectPath, defaultProjectPath)
  )
  const outputRoot = path.resolve(
    replaceProjectRootPlaceholders(rawConfig.outputRoot || defaultOutputRoot, projectPath)
  )
  const routes = Array.isArray(rawConfig.routes)
    ? rawConfig.routes.map((route) => normalizeConfigRoute(route, projectPath))
    : []

  if (!routes.length) {
    throw new Error('Config must define at least one route')
  }

  return {
    configPath,
    outputRoot,
    projectPath,
    routes,
  }
}

function validateProjectPath(projectPath) {
  const projectConfigPath = path.join(projectPath, 'project.config.json')

  if (!fs.existsSync(projectConfigPath)) {
    throw new Error(
      `projectPath must point to a WeChat Mini Program project root containing project.config.json: ${projectPath}`
    )
  }

  const projectConfig = readJsonFile(projectConfigPath, projectConfigPath)
  const miniprogramRoot =
    typeof projectConfig.miniprogramRoot === 'string' && projectConfig.miniprogramRoot.trim()
      ? projectConfig.miniprogramRoot
      : '.'
  const miniappRoot = path.resolve(projectPath, miniprogramRoot)
  const appJsonPath = path.join(miniappRoot, 'app.json')

  if (!fs.existsSync(appJsonPath)) {
    throw new Error(
      `Resolved miniapp root is missing app.json. projectPath=${projectPath}, miniprogramRoot=${miniprogramRoot}`
    )
  }

  return {
    appJsonPath,
    miniappRoot,
    miniprogramRoot,
    projectConfigPath,
  }
}

function probeCliPath(cliPath) {
  const resolvedPath = typeof cliPath === 'string' ? cliPath.trim() : ''

  if (!resolvedPath) {
    return {
      available: false,
      error: 'WeChat DevTools cli.bat path is empty. Pass --cli-path or set WECHAT_DEVTOOLS_CLI_PATH.',
      path: '',
    }
  }

  if (!fs.existsSync(resolvedPath)) {
    return {
      available: false,
      error: `WeChat DevTools CLI not found at: ${resolvedPath}`,
      path: resolvedPath,
    }
  }

  return {
    available: true,
    error: '',
    path: resolvedPath,
  }
}

function probeAutomator(options) {
  try {
    const { source } = loadAutomator(options)
    return {
      available: true,
      error: '',
      source,
    }
  } catch (error) {
    return {
      available: false,
      error: error && error.message ? error.message : String(error),
      source: '',
    }
  }
}

function summarizeSpec(spec) {
  return {
    actionCount: Array.isArray(spec.actions) ? spec.actions.length : 0,
    actionTypes: Array.isArray(spec.actions) ? spec.actions.map((action) => action.type) : [],
    expectedPath: spec.expectedPath,
    key: spec.key,
    primarySelector: spec.primarySelector,
    route: spec.route,
    titleSelector: spec.titleSelector,
  }
}

function selectSpecs(routeArgs, specs) {
  if (!routeArgs.length) {
    return specs
  }

  const requested = new Set(routeArgs)
  return specs.filter((spec) => requested.has(spec.key) || requested.has(spec.route))
}

function flattenConsoleArgs(payload) {
  if (!payload || !Array.isArray(payload.args)) {
    return ''
  }

  return payload.args
    .map((item) => {
      if (!item) {
        return ''
      }

      if (typeof item.value !== 'undefined') {
        return String(item.value)
      }

      if (typeof item.description !== 'undefined') {
        return String(item.description)
      }

      return JSON.stringify(item)
    })
    .join(' ')
}

function normalizeConsoleEvent(payload) {
  return {
    type: payload && payload.type ? payload.type : '',
    source: payload && payload.source ? payload.source : '',
    level: payload && payload.level ? payload.level : '',
    text: flattenConsoleArgs(payload),
    raw: safeSerialize(payload),
  }
}

function normalizeExceptionEvent(payload) {
  const details = payload && payload.details ? payload.details : {}

  return {
    text: details.text || payload.text || '',
    stack: details.stackTrace || null,
    raw: safeSerialize(payload),
  }
}

function createIssue(code, message) {
  return {
    code,
    message,
  }
}

function issueMessages(issues) {
  return issues.map((issue) => issue.message)
}

function uniqueIssueCodes(issues) {
  return Array.from(new Set(issues.map((issue) => issue.code)))
}

function countIssuesByCode(issues) {
  const counts = {}

  for (const issue of issues) {
    counts[issue.code] = (counts[issue.code] || 0) + 1
  }

  return counts
}

async function inspectImage(imagePath) {
  const image = PNG.sync.read(fs.readFileSync(imagePath))
  const { width, height, data } = image
  const stepX = Math.max(1, Math.floor(width / 80))
  const stepY = Math.max(1, Math.floor(height / 160))

  let visibleCount = 0
  let sum = 0
  let sumSquares = 0
  let nonWhiteCount = 0

  for (let y = 0; y < height; y += stepY) {
    for (let x = 0; x < width; x += stepX) {
      const index = (width * y + x) * 4
      const rgba = {
        r: data[index],
        g: data[index + 1],
        b: data[index + 2],
        a: data[index + 3],
      }

      if (rgba.a < 10) {
        continue
      }

      visibleCount += 1

      const luminance = 0.2126 * rgba.r + 0.7152 * rgba.g + 0.0722 * rgba.b
      sum += luminance
      sumSquares += luminance * luminance

      if (luminance < 245) {
        nonWhiteCount += 1
      }
    }
  }

  const mean = visibleCount ? sum / visibleCount : 255
  const variance = visibleCount ? Math.max(0, sumSquares / visibleCount - mean * mean) : 0
  const stddev = Math.sqrt(variance)
  const nonWhiteRatio = visibleCount ? nonWhiteCount / visibleCount : 0

  return {
    width,
    height,
    visibleCount,
    meanLuminance: Number(mean.toFixed(2)),
    luminanceStddev: Number(stddev.toFixed(2)),
    nonWhiteRatio: Number(nonWhiteRatio.toFixed(4)),
    possibleBlank: stddev < 8 && nonWhiteRatio < 0.03,
  }
}

function stopLauncherProcess(child) {
  if (!child || child.exitCode !== null || child.killed) {
    return
  }

  try {
    child.kill()
  } catch (error) {}
}

async function startAutomationCli(options, runDir) {
  const commandParts = [
    `& '${String(options.cliPath).replace(/'/g, "''")}'`,
    'auto',
    `--project '${String(options.projectPath).replace(/'/g, "''")}'`,
    `--auto-port ${String(options.port)}`,
  ]

  if (options.trustProject) {
    commandParts.push('--trust-project')
  }

  const commandLine = commandParts.join(' ')

  return new Promise((resolve, reject) => {
    const child = childProcess.spawn('powershell.exe', ['-NoProfile', '-Command', commandLine], {
      stdio: ['ignore', 'pipe', 'pipe'],
      windowsHide: true,
    })

    let stdout = ''
    let stderr = ''
    let settled = false

    const launchTimeout = setTimeout(() => {
      appendRunTrace(
        runDir,
        `cli auto did not exit within ${DEFAULT_CLI_LAUNCH_TIMEOUT_MS}ms; continuing while DevTools finishes booting in the background`
      )

      if (child.stdout && !child.stdout.destroyed) {
        child.stdout.removeAllListeners('data')
        child.stdout.destroy()
      }

      if (child.stderr && !child.stderr.destroyed) {
        child.stderr.removeAllListeners('data')
        child.stderr.destroy()
      }

      child.unref()
      settled = true
      resolve({
        child,
        mode: 'backgrounded',
      })
    }, DEFAULT_CLI_LAUNCH_TIMEOUT_MS)

    child.stdout.on('data', (chunk) => {
      stdout += String(chunk)
    })

    child.stderr.on('data', (chunk) => {
      stderr += String(chunk)
    })

    child.on('error', (error) => {
      if (settled) {
        return
      }

      clearTimeout(launchTimeout)
      settled = true
      reject(error)
    })
    child.on('exit', (code) => {
      if (settled) {
        return
      }

      clearTimeout(launchTimeout)

      if (code === 0) {
        settled = true
        resolve({
          child: null,
          mode: 'exited',
        })
        return
      }

      settled = true
      reject(new Error(`cli auto exited with code ${code}\nstdout:\n${stdout.trim()}\nstderr:\n${stderr.trim()}`))
    })
  })
}

async function connectWithRetry(automator, port, timeoutMs) {
  const wsEndpoint = `ws://127.0.0.1:${port}`
  const deadline = Date.now() + timeoutMs
  let lastError = null

  while (Date.now() < deadline) {
    try {
      return await automator.connect({ wsEndpoint })
    } catch (error) {
      lastError = error
      await sleep(1000)
    }
  }

  if (lastError) {
    throw new Error(
      [
        `Failed connecting to ${wsEndpoint}.`,
        'DevTools may have reused an old session or kept a blocking dialog open.',
        `Original error: ${lastError.message || String(lastError)}`,
      ].join(' ')
    )
  }

  throw new Error(`Failed connecting to ${wsEndpoint}`)
}

async function waitForAppReady(miniProgram, timeoutMs) {
  const deadline = Date.now() + timeoutMs
  let lastError = null

  while (Date.now() < deadline) {
    try {
      const page = await withTimeout('warm app currentPage', 6000, () => miniProgram.currentPage())

      if (page) {
        await sleep(1200)
        return page
      }
    } catch (error) {
      lastError = error
    }

    await sleep(1500)
  }

  throw new Error(
    [
      'Mini program runtime did not become ready after automation connected.',
      lastError ? `Last error: ${lastError.message || String(lastError)}` : '',
    ]
      .filter(Boolean)
      .join(' ')
  )
}

async function openPage(miniProgram, spec) {
  const route = spec.route
  const normalizedExpectedPath = spec.expectedPath
  const currentPage = await withTimeout(`read currentPage before open ${route}`, 8000, () => miniProgram.currentPage())

  if (currentPage && currentPage.path === normalizedExpectedPath) {
    await withTimeout(`settle current page ${route}`, 8000, () => currentPage.waitFor(spec.settleMs))
    return currentPage
  }

  const page = await withTimeout(`openPage ${route}`, 15000, () => miniProgram.reLaunch(route))

  if (!page) {
    throw new Error(`Failed to open route ${route}`)
  }

  await withTimeout(`settle page ${route}`, 12000, () => page.waitFor(spec.settleMs))
  return page
}

async function capturePageBasics(page, spec) {
  const result = {
    path: page.path,
    query: safeSerialize(page.query),
  }

  const shell = spec.primarySelector ? await page.$(spec.primarySelector) : null
  result.hasPrimarySelector = Boolean(shell)

  if (shell) {
    result.primarySize = safeSerialize(await shell.size())
  }

  if (spec.titleSelector) {
    const titleNode = await page.$(spec.titleSelector)
    result.titleText = titleNode ? await titleNode.text() : ''
  }

  const data = await page.data()
  result.selectedData = pickDataFields(data, spec.dataFields)
  result.loading = data && typeof data.loading !== 'undefined' ? Boolean(data.loading) : null
  result.errorMessage = data && data.errorMessage ? String(data.errorMessage) : ''

  return result
}

async function resolveActionNode(page, action) {
  if (!action.selector) {
    return null
  }

  if (action.all || typeof action.index === 'number') {
    const nodes = await page.$$(action.selector)
    const index = typeof action.index === 'number' ? action.index : 0
    return Array.isArray(nodes) ? nodes[index] || null : null
  }

  return page.$(action.selector)
}

async function runActionSequence(page, actions) {
  const results = []

  for (const action of actions) {
    if (action.type === 'wait') {
      await page.waitFor(action.waitMs || 500)
      results.push({
        type: 'wait',
        ok: true,
        waitMs: action.waitMs || 500,
        required: action.required,
      })
      continue
    }

    if (action.type === 'tap') {
      const node = await resolveActionNode(page, action)

      if (!node) {
        results.push({
          type: 'tap',
          selector: action.selector || '',
          index: typeof action.index === 'number' ? action.index : undefined,
          ok: false,
          required: action.required,
          reason: `missing selector ${action.selector || '<empty>'}`,
        })
        continue
      }

      await node.tap()

      if (action.waitMs > 0) {
        await page.waitFor(action.waitMs)
      }

      results.push({
        type: 'tap',
        selector: action.selector || '',
        index: typeof action.index === 'number' ? action.index : undefined,
        ok: true,
        required: action.required,
      })
      continue
    }

    if (action.type === 'callMethod') {
      if (!action.method) {
        results.push({
          type: 'callMethod',
          ok: false,
          required: action.required,
          reason: 'missing method name',
        })
        continue
      }

      await withTimeout(`call ${action.method}`, 10000, () => page.callMethod(action.method, action.payload))

      if (action.waitMs > 0) {
        await page.waitFor(action.waitMs)
      }

      results.push({
        type: 'callMethod',
        method: action.method,
        ok: true,
        required: action.required,
      })
      continue
    }

    results.push({
      type: action.type || 'unknown',
      ok: false,
      required: false,
      reason: `unsupported action type ${action.type || '<empty>'}`,
    })
  }

  return results
}

async function runSpec({ miniProgram, spec, runDir, consoleEvents, exceptionEvents }) {
  console.log(`[gui-check] start ${spec.key} ${spec.route}`)
  appendRunTrace(runDir, `start spec ${spec.key} ${spec.route}`)

  const consoleStart = consoleEvents.length
  const exceptionStart = exceptionEvents.length
  const page = await openPage(miniProgram, spec)
  const details = await withTimeout(`capture basics ${spec.key}`, 15000, () => capturePageBasics(page, spec))
  const actionResults = await withTimeout(`actions ${spec.key}`, 30000, () => runActionSequence(page, spec.actions))
  const currentPage = await withTimeout(`currentPage ${spec.key}`, 10000, () => miniProgram.currentPage())
  const finalPath = currentPage ? currentPage.path : ''
  const screenshotPath = path.join(runDir, `${spec.key}.png`)
  const newConsoleEvents = consoleEvents.slice(consoleStart)
  const newExceptionEvents = exceptionEvents.slice(exceptionStart)
  const severeConsoleEvents = newConsoleEvents.filter(isSevereConsoleEvent)
  const failureDetails = []
  const warningDetails = []
  let imageMetrics = null
  let screenshotSaved = false

  try {
    await withTimeout(`screenshot ${spec.key}`, 30000, () => miniProgram.screenshot({ path: screenshotPath }))
    screenshotSaved = true
    imageMetrics = await withTimeout(`inspect image ${spec.key}`, 15000, () => inspectImage(screenshotPath))
  } catch (error) {
    const message = `screenshot unavailable: ${error && error.message ? error.message : String(error)}`
    warningDetails.push(createIssue(classifyScreenshotWarning(message), message))
  }

  if (spec.expectedPath && finalPath !== spec.expectedPath) {
    failureDetails.push(createIssue('repo_runtime_error', `final path mismatch: ${finalPath || '<empty>'}`))
  }

  if (spec.primarySelector && !details.hasPrimarySelector) {
    failureDetails.push(createIssue('selector_assertion_error', `missing selector ${spec.primarySelector}`))
  }

  if (details.errorMessage) {
    failureDetails.push(createIssue('repo_runtime_error', `page data errorMessage: ${details.errorMessage}`))
  }

  if (newExceptionEvents.length) {
    failureDetails.push(createIssue('repo_runtime_error', `runtime exceptions: ${newExceptionEvents.length}`))
  }

  if (severeConsoleEvents.length) {
    failureDetails.push(createIssue('repo_runtime_error', `severe console events: ${severeConsoleEvents.length}`))
  }

  for (const result of actionResults) {
    if (result.ok === false && result.required !== false) {
      failureDetails.push(createIssue(classifyActionFailure(result), result.reason || `${result.type} failed`))
    }

    if (result.ok === false && result.required === false) {
      warningDetails.push(
        createIssue(classifyActionFailure(result), `non-required action failed: ${result.reason || result.type}`)
      )
    }
  }

  if (imageMetrics && imageMetrics.possibleBlank) {
    warningDetails.push(createIssue('repo_runtime_error', 'possible blank or nearly blank screenshot'))
  }

  const result = {
    key: spec.key,
    route: spec.route,
    expectedPath: spec.expectedPath,
    finalPath,
    ok: failureDetails.length === 0,
    details,
    actionResults,
    screenshotPath: screenshotSaved ? screenshotPath : '',
    imageMetrics,
    failureCodes: uniqueIssueCodes(failureDetails),
    warningCodes: uniqueIssueCodes(warningDetails),
    failureDetails,
    warningDetails,
    failures: issueMessages(failureDetails),
    warnings: issueMessages(warningDetails),
    consoleEvents: newConsoleEvents,
    exceptionEvents: newExceptionEvents,
  }

  console.log(`[gui-check] finish ${spec.key} ok=${result.ok}`)
  appendRunTrace(
    runDir,
    `finish spec ${spec.key} ok=${result.ok} failures=${result.failureDetails.length} warnings=${result.warningDetails.length}`
  )
  return result
}

async function main() {
  const options = parseArgs(process.argv.slice(2))
  const config = loadConfig(options.configPath, options.projectPath, options.outputRoot)
  const selectedSpecs = selectSpecs(options.routes, config.routes)
  const projectInfo = validateProjectPath(config.projectPath)
  const cli = probeCliPath(options.cliPath)
  const automator = probeAutomator({
    automatorModulePath: options.automatorModulePath,
    projectPath: config.projectPath,
  })

  if (!selectedSpecs.length) {
    throw new Error('No routes selected')
  }

  if (options.dryRun) {
    const classifiedCli = {
      ...cli,
      classification: classifyCliProbe(cli),
    }
    const classifiedAutomator = {
      ...automator,
      classification: classifyAutomatorProbe(automator),
    }

    console.log(
      JSON.stringify(
        {
          automator: classifiedAutomator,
          cli: classifiedCli,
          configPath: config.configPath,
          mode: 'dry-run',
          ok: true,
          outputRoot: config.outputRoot,
          project: projectInfo,
          projectPath: config.projectPath,
          readyForAutomation: Boolean(cli.available && automator.available),
          selectedRoutes: selectedSpecs.map((spec) => summarizeSpec(spec)),
        },
        null,
        2
      )
    )
    return
  }

  if (!cli.available) {
    throw new Error(cli.error)
  }

  if (!automator.available) {
    throw new Error(automator.error)
  }

  const { automator: automatorModule, source: automatorSource } = loadAutomator({
    automatorModulePath: options.automatorModulePath,
    projectPath: config.projectPath,
  })

  const runDir = path.join(config.outputRoot, timestampSlug())
  ensureDir(runDir)
  appendRunTrace(runDir, `selected routes: ${selectedSpecs.map((spec) => spec.key).join(', ')}`)
  appendRunTrace(runDir, `config path: ${config.configPath}`)
  appendRunTrace(runDir, `project path: ${config.projectPath}`)

  const consoleEvents = []
  const exceptionEvents = []
  let miniProgram = null
  let cliLaunchRuntime = {
    child: null,
    mode: 'not-started',
  }

  try {
    appendRunTrace(runDir, `launching DevTools CLI on port ${options.port}`)
    cliLaunchRuntime = await startAutomationCli(
      {
        cliPath: cli.path,
        port: options.port,
        projectPath: config.projectPath,
        trustProject: options.trustProject,
      },
      runDir
    )
    appendRunTrace(runDir, `DevTools CLI launch mode: ${cliLaunchRuntime.mode}`)

    await sleep(1500)
    appendRunTrace(runDir, `connecting automator websocket ws://127.0.0.1:${options.port}`)
    miniProgram = await connectWithRetry(automatorModule, options.port, 30000)
    appendRunTrace(runDir, 'automator websocket connected')
    await waitForAppReady(miniProgram, 45000)
    appendRunTrace(runDir, 'mini program runtime ready')

    miniProgram.on('console', (payload) => {
      consoleEvents.push(normalizeConsoleEvent(payload))
    })

    miniProgram.on('exception', (payload) => {
      exceptionEvents.push(normalizeExceptionEvent(payload))
    })

    const report = {
      configPath: config.configPath,
      generatedAt: new Date().toISOString(),
      reportSchemaVersion: 2,
      pages: [],
      project: {
        appJsonPath: projectInfo.appJsonPath,
        automatorSource,
        miniappRoot: projectInfo.miniappRoot,
        miniprogramRoot: projectInfo.miniprogramRoot,
        projectConfigPath: projectInfo.projectConfigPath,
      },
      projectPath: config.projectPath,
      runDir,
      summary: {
        total: 0,
        passed: 0,
        failed: 0,
        warningPages: 0,
        failureClassCounts: {},
        warningClassCounts: {},
      },
    }

    try {
      for (const spec of selectedSpecs) {
        let pageReport

        try {
          pageReport = await runSpec({
            miniProgram,
            spec,
            runDir,
            consoleEvents,
            exceptionEvents,
          })
        } catch (error) {
          const message = error && error.message ? error.message : String(error)
          const failureDetails = [createIssue(classifyRunSpecErrorMessage(message), message)]

          pageReport = {
            key: spec.key,
            route: spec.route,
            expectedPath: spec.expectedPath,
            finalPath: '',
            ok: false,
            details: null,
            actionResults: [],
            screenshotPath: '',
            imageMetrics: null,
            failureCodes: uniqueIssueCodes(failureDetails),
            warningCodes: [],
            failureDetails,
            warningDetails: [],
            failures: issueMessages(failureDetails),
            warnings: [],
            consoleEvents: consoleEvents.slice(),
            exceptionEvents: exceptionEvents.slice(),
          }
          appendRunTrace(runDir, `fail spec ${spec.key}: ${message}`)
        }

        report.pages.push(pageReport)
        fs.writeFileSync(path.join(runDir, 'report.partial.json'), JSON.stringify(report, null, 2))
      }
    } finally {
      if (miniProgram) {
        if (!options.keepOpen) {
          await withTimeout('close miniProgram', 10000, () => miniProgram.close()).catch(() => {})
        }

        if (typeof miniProgram.disconnect === 'function') {
          miniProgram.disconnect()
        }
      }

      stopLauncherProcess(cliLaunchRuntime.child)
    }

    report.summary.total = report.pages.length
    report.summary.passed = report.pages.filter((page) => page.ok).length
    report.summary.failed = report.summary.total - report.summary.passed
    report.summary.warningPages = report.pages.filter((page) => page.warnings.length > 0).length
    report.summary.failureClassCounts = countIssuesByCode(
      report.pages.flatMap((page) => page.failureDetails || [])
    )
    report.summary.warningClassCounts = countIssuesByCode(
      report.pages.flatMap((page) => page.warningDetails || [])
    )

    const reportPath = path.join(runDir, 'report.json')
    fs.writeFileSync(reportPath, JSON.stringify(report, null, 2))
    appendRunTrace(
      runDir,
      `summary total=${report.summary.total} passed=${report.summary.passed} failed=${report.summary.failed} warningPages=${report.summary.warningPages}`
    )
    console.log(JSON.stringify(report, null, 2))

    if (report.summary.failed > 0) {
      process.exitCode = 1
    }
  } finally {
    stopLauncherProcess(cliLaunchRuntime.child)
  }
}

main().catch((error) => {
  const message = error && error.message ? error.message : String(error)

  console.error(
    JSON.stringify(
      {
        ok: false,
        classification: classifyFatalErrorMessage(message),
        error: message,
        stack: error && error.stack ? error.stack : null,
      },
      null,
      2
    )
  )
  process.exitCode = 1
})
