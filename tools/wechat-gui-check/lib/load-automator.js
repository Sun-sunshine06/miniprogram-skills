const fs = require('fs')
const path = require('path')
const { createRequire } = require('module')

function tryRequireWithFactory(requireFactory, specifier) {
  try {
    return {
      module: requireFactory(specifier),
      ok: true,
    }
  } catch (error) {
    return {
      error,
      ok: false,
    }
  }
}

function buildCandidateList({ automatorModulePath, projectPath }) {
  const candidates = []

  if (automatorModulePath) {
    const explicitPath = path.resolve(automatorModulePath)

    if (fs.existsSync(explicitPath) && fs.statSync(explicitPath).isDirectory()) {
      const explicitRequire = createRequire(path.join(explicitPath, 'package.json'))
      candidates.push({
        label: `explicit package directory ${explicitPath}`,
        load() {
          return tryRequireWithFactory(explicitRequire, 'miniprogram-automator')
        },
      })
    }

    candidates.push({
      label: `explicit module path ${explicitPath}`,
      load() {
        return tryRequireWithFactory(require, explicitPath)
      },
    })
  }

  if (projectPath) {
    const projectRequire = createRequire(path.join(projectPath, 'package.json'))
    candidates.push({
      label: `project-local dependency from ${projectPath}`,
      load() {
        return tryRequireWithFactory(projectRequire, 'miniprogram-automator')
      },
    })
  }

  candidates.push({
    label: 'local wechat-gui-check dependency',
    load() {
      return tryRequireWithFactory(require, 'miniprogram-automator')
    },
  })

  return candidates
}

function formatMissingAutomatorError(errors) {
  const lines = [
    'Unable to load `miniprogram-automator` for GUI automation.',
    'Tried:',
    ...errors.map((item) => `- ${item.label}: ${item.message}`),
    'Install it in the target miniapp project with `npm install --no-save miniprogram-automator`,',
    'or pass `--automator-module-path <path>` / set `WECHAT_GUI_CHECK_AUTOMATOR_PATH` to an existing install.',
  ]

  return new Error(lines.join('\n'))
}

function loadAutomator(options) {
  const errors = []

  for (const candidate of buildCandidateList(options)) {
    const attempt = candidate.load()

    if (attempt.ok) {
      return {
        automator: attempt.module,
        source: candidate.label,
      }
    }

    errors.push({
      label: candidate.label,
      message: attempt.error && attempt.error.message ? attempt.error.message : String(attempt.error),
    })
  }

  throw formatMissingAutomatorError(errors)
}

module.exports = {
  loadAutomator,
}
