const fs = require('fs')

const DEFAULT_CLI_CANDIDATES = [
  process.env.WECHAT_DEVTOOLS_CLI_PATH || '',
  'D:\\微信web开发者工具\\cli.bat',
  'D:\\develop\\微信web开发者工具\\cli.bat',
  'C:\\Program Files (x86)\\Tencent\\微信web开发者工具\\cli.bat',
  'C:\\Program Files\\Tencent\\微信web开发者工具\\cli.bat',
  'C:\\Program Files (x86)\\Tencent\\Wechatwebdevtools\\cli.bat',
  'C:\\Program Files\\Tencent\\Wechatwebdevtools\\cli.bat',
].filter(Boolean)

function pickFirstExistingPath(candidates, exists = fs.existsSync) {
  for (const candidate of candidates) {
    if (candidate && exists(candidate)) {
      return candidate
    }
  }

  return candidates[0] || ''
}

function resolveDefaultCliPath(exists = fs.existsSync) {
  return pickFirstExistingPath(DEFAULT_CLI_CANDIDATES, exists)
}

function isSevereConsoleEvent(event) {
  const type = String(event && event.type ? event.type : '').toLowerCase()
  const level = String(event && event.level ? event.level : '').toLowerCase()
  const text = String(event && event.text ? event.text : '').toLowerCase()

  if (type === 'warn' || type === 'warning' || level === 'warn' || level === 'warning') {
    return text.includes('typeerror') || text.includes('referenceerror')
  }

  return (
    type === 'error' ||
    level === 'error' ||
    text.includes('exception') ||
    text.includes('typeerror') ||
    text.includes('referenceerror')
  )
}

function getByPath(input, pathExpression) {
  if (!pathExpression) {
    return undefined
  }

  const segments = String(pathExpression).split('.').filter(Boolean)
  let current = input

  for (const segment of segments) {
    if (current == null || typeof current !== 'object') {
      return undefined
    }

    current = current[segment]
  }

  return current
}

function pickDataFields(data, fields) {
  const output = {}

  for (const field of Array.isArray(fields) ? fields : []) {
    output[field] = getByPath(data, field)
  }

  return output
}

module.exports = {
  DEFAULT_CLI_CANDIDATES,
  getByPath,
  isSevereConsoleEvent,
  pickDataFields,
  pickFirstExistingPath,
  resolveDefaultCliPath,
}
