function classifyCliProbe(cli) {
  return cli && cli.available ? 'ok' : 'environment_error'
}

function classifyAutomatorProbe(automator) {
  return automator && automator.available ? 'ok' : 'automation_dependency_missing'
}

function classifyScreenshotWarning(message) {
  const normalized = String(message || '').toLowerCase()

  if (normalized.includes('timed out')) {
    return 'screenshot_timeout'
  }

  if (
    normalized.includes('not a function') ||
    normalized.includes('not implemented') ||
    normalized.includes('not supported') ||
    normalized.includes('unsupported')
  ) {
    return 'screenshot_capability_missing'
  }

  return 'devtools_session_error'
}

function classifyActionFailure(result) {
  const reason = String(result && result.reason ? result.reason : '').toLowerCase()

  if (reason.includes('missing selector') || result.type === 'tap') {
    return 'selector_assertion_error'
  }

  return 'repo_runtime_error'
}

function classifyFatalErrorMessage(message) {
  const normalized = String(message || '').toLowerCase()

  if (normalized.includes('miniprogram-automator')) {
    return 'automation_dependency_missing'
  }

  if (
    normalized.includes('cli.bat path is empty') ||
    normalized.includes('devtools cli not found') ||
    normalized.includes('projectpath must point') ||
    normalized.includes('missing app.json') ||
    normalized.includes('failed parsing') ||
    normalized.includes('config must define at least one route') ||
    normalized.includes('no routes selected')
  ) {
    return 'environment_error'
  }

  if (
    normalized.includes('cli auto exited') ||
    normalized.includes('failed connecting to ws://') ||
    normalized.includes('blocking dialog') ||
    normalized.includes('did not become ready')
  ) {
    return 'devtools_session_error'
  }

  return 'environment_error'
}

function classifyRunSpecErrorMessage(message) {
  const normalized = String(message || '').toLowerCase()

  if (normalized.includes('missing selector')) {
    return 'selector_assertion_error'
  }

  if (
    normalized.includes('failed to open route') ||
    normalized.includes('capture basics') ||
    normalized.includes('actions ') ||
    normalized.includes('call ')
  ) {
    return 'repo_runtime_error'
  }

  const topLevelCode = classifyFatalErrorMessage(message)

  if (topLevelCode === 'environment_error') {
    return 'devtools_session_error'
  }

  return topLevelCode
}

module.exports = {
  classifyActionFailure,
  classifyAutomatorProbe,
  classifyCliProbe,
  classifyFatalErrorMessage,
  classifyRunSpecErrorMessage,
  classifyScreenshotWarning,
}
