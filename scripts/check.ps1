param(
    [switch]$IncludeAudit
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (Resolve-Path (Join-Path $ScriptRoot '..')).Path
$ToolRoot = Join-Path $RepoRoot 'tools\wechat-gui-check'
$FixtureRoot = Join-Path $ToolRoot 'examples\fixture-miniapp'
$SampleConfigPath = Join-Path $ToolRoot 'examples\sample.route-config.json'
$RichSampleConfigPath = Join-Path $ToolRoot 'examples\sample.rich.route-config.json'
$SampleReportPath = Join-Path $ToolRoot 'examples\sample-report.json'

function Assert-Command {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Name
    )

    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "Missing required command on PATH: $Name"
    }
}

function Invoke-Step {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Name,

        [Parameter(Mandatory = $true)]
        [scriptblock]$Action
    )

    Write-Host ''
    Write-Host "==> $Name"
    & $Action
}

function Invoke-Native {
    param(
        [Parameter(Mandatory = $true)]
        [string]$FilePath,

        [Parameter(Mandatory = $true)]
        [string[]]$Arguments,

        [string]$WorkingDirectory = $RepoRoot
    )

    $commandLine = "$FilePath $($Arguments -join ' ')"
    Push-Location $WorkingDirectory
    try {
        & $FilePath @Arguments
        $exitCode = $LASTEXITCODE
    }
    finally {
        Pop-Location
    }

    if ($exitCode -ne 0) {
        throw "Command failed with exit code ${exitCode}: $commandLine"
    }
}

function Invoke-NativeCapture {
    param(
        [Parameter(Mandatory = $true)]
        [string]$FilePath,

        [Parameter(Mandatory = $true)]
        [string[]]$Arguments,

        [string]$WorkingDirectory = $RepoRoot
    )

    $commandLine = "$FilePath $($Arguments -join ' ')"
    Push-Location $WorkingDirectory
    try {
        $output = & $FilePath @Arguments 2>&1
        $exitCode = $LASTEXITCODE
    }
    finally {
        Pop-Location
    }

    if ($exitCode -ne 0) {
        $text = ($output | ForEach-Object { $_.ToString() }) -join [Environment]::NewLine
        throw "Command failed with exit code ${exitCode}: $commandLine`n$text"
    }

    return ($output | ForEach-Object { $_.ToString() }) -join [Environment]::NewLine
}

function Assert-PathsExist {
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$Paths
    )

    foreach ($PathItem in $Paths) {
        if (-not (Test-Path -LiteralPath $PathItem)) {
            throw "Expected file not found: $PathItem"
        }
    }
}

function New-TempDirectory {
    $tempPath = Join-Path ([System.IO.Path]::GetTempPath()) ("miniprogram-skills-check-" + [Guid]::NewGuid().ToString('N'))
    New-Item -ItemType Directory -Path $tempPath | Out-Null
    return $tempPath
}

Assert-Command python
Assert-Command node
Assert-Command npm

$jsonValidationScript = @'
const fs = require('fs');

for (const file of process.argv.slice(1)) {
  JSON.parse(fs.readFileSync(file, 'utf8'));
}
'@

$runtimeImportScript = @'
const { PNG } = require('pngjs');

if (typeof PNG.sync.read !== 'function') {
  throw new Error('pngjs PNG.sync.read unavailable');
}
'@

$automatorGuidanceScript = @'
const { loadAutomator } = require('./lib/load-automator');

try {
  loadAutomator({ projectPath: process.cwd() });
  throw new Error('expected missing miniprogram-automator guidance');
} catch (error) {
  if (!String(error.message).includes('miniprogram-automator')) {
    throw error;
  }
}
'@

$classificationScript = @'
const { classifyScreenshotWarning } = require('./lib/classification');

if (classifyScreenshotWarning('screenshot unavailable: miniProgram.screenshot is not a function') !== 'screenshot_capability_missing') {
  throw new Error('expected screenshot capability classification');
}

if (classifyScreenshotWarning('screenshot unavailable: screenshot timed out after 30000ms') !== 'screenshot_timeout') {
  throw new Error('expected screenshot timeout classification');
}
'@

$dryRunValidationScript = @'
const fs = require('fs');

const report = JSON.parse(fs.readFileSync(process.argv[1], 'utf8'));

if (!report.ok || report.mode !== 'dry-run') {
  throw new Error('unexpected dry-run result');
}

if (!report.project || !String(report.project.projectConfigPath).endsWith('project.config.json')) {
  throw new Error('missing project info');
}

if (!Array.isArray(report.selectedRoutes) || report.selectedRoutes.length !== 1 || report.selectedRoutes[0].key !== 'home') {
  throw new Error('wrong route selection');
}

if (report.automator.available !== false || !String(report.automator.error).includes('miniprogram-automator')) {
  throw new Error('expected missing automator guidance');
}
'@

$richDryRunValidationScript = @'
const fs = require('fs');

const report = JSON.parse(fs.readFileSync(process.argv[1], 'utf8'));

if (!report.ok || report.mode !== 'dry-run') {
  throw new Error('unexpected richer dry-run result');
}

if (!String(report.configPath).endsWith('sample.rich.route-config.json')) {
  throw new Error('wrong richer config path');
}

if (!Array.isArray(report.selectedRoutes) || report.selectedRoutes.length !== 1) {
  throw new Error('wrong richer route selection size');
}

const selected = report.selectedRoutes[0];

if (selected.key !== 'home-rich-actions') {
  throw new Error('wrong richer route key');
}

if (selected.actionCount !== 3) {
  throw new Error('wrong richer action count');
}

if (JSON.stringify(selected.actionTypes) !== JSON.stringify(['wait', 'tap', 'callMethod'])) {
  throw new Error('wrong richer action types');
}

if (report.automator.available !== false || !String(report.automator.error).includes('miniprogram-automator')) {
  throw new Error('expected missing automator guidance');
}
'@

Invoke-Step 'Validate skills' {
    Invoke-Native 'python' @(
        (Join-Path $RepoRoot 'scripts\validate_skills.py'),
        (Join-Path $RepoRoot 'skills'),
        '--require-example-prompts',
        '--check-portability'
    )
}

Invoke-Step 'Validate docs' {
    Invoke-Native 'python' @(
        (Join-Path $RepoRoot 'scripts\validate_docs.py'),
        $RepoRoot
    )
}

Invoke-Step 'Install tool dependencies' {
    Invoke-Native 'npm' @('ci', '--ignore-scripts') $ToolRoot
}

Invoke-Step 'Check tool syntax' {
    Invoke-Native 'node' @('--check', (Join-Path $ToolRoot 'check.js'))
    Invoke-Native 'node' @('--check', (Join-Path $ToolRoot 'lib\check-helpers.js'))
    Invoke-Native 'node' @('--check', (Join-Path $ToolRoot 'lib\classification.js'))
    Invoke-Native 'node' @('--check', (Join-Path $ToolRoot 'lib\load-automator.js'))
}

Invoke-Step 'Validate repository JSON' {
    $jsonFiles = Get-ChildItem -Path $RepoRoot -Recurse -File -Filter *.json |
        Where-Object {
            $_.FullName -notmatch '\\node_modules\\' -and
            $_.FullName -notmatch '\\\.git\\' -and
            $_.FullName -notmatch '\\\.tmp\\'
        } |
        ForEach-Object { $_.FullName }

    Invoke-Native 'node' (@(
        '-e',
        $jsonValidationScript
    ) + $jsonFiles)
}

Invoke-Step 'Check runtime imports' {
    Invoke-Native 'node' @('-e', $runtimeImportScript) $ToolRoot
    Invoke-Native 'node' @('-e', $automatorGuidanceScript) $ToolRoot
    Invoke-Native 'node' @('-e', $classificationScript) $ToolRoot
}

Invoke-Step 'Check bundled fixture files' {
    Assert-PathsExist @(
        (Join-Path $FixtureRoot 'project.config.json'),
        (Join-Path $FixtureRoot 'app.json'),
        (Join-Path $FixtureRoot 'pages\home\index.wxml'),
        (Join-Path $FixtureRoot 'pages\tasks\index.wxml')
    )
}

Invoke-Step 'Check external-project dry run' {
    $tempRoot = New-TempDirectory
    $utf8NoBom = New-Object System.Text.UTF8Encoding -ArgumentList $false

    try {
        $copiedFixtureRoot = Join-Path $tempRoot 'fixture-miniapp'
        $preflightPath = Join-Path $tempRoot 'preflight.json'
        $richPreflightPath = Join-Path $tempRoot 'preflight.rich.json'
        Copy-Item -LiteralPath $FixtureRoot -Destination $copiedFixtureRoot -Recurse

        $preflightOutput = Invoke-NativeCapture 'node' @(
            (Join-Path $ToolRoot 'check.js'),
            '--config',
            $SampleConfigPath,
            '--project-path',
            $copiedFixtureRoot,
            '--route',
            'home',
            '--dry-run'
        )

        [System.IO.File]::WriteAllText($preflightPath, $preflightOutput, $utf8NoBom)

        Invoke-Native 'node' @(
            '-e',
            $dryRunValidationScript,
            $preflightPath
        )

        $richPreflightOutput = Invoke-NativeCapture 'node' @(
            (Join-Path $ToolRoot 'check.js'),
            '--config',
            $RichSampleConfigPath,
            '--project-path',
            $copiedFixtureRoot,
            '--route',
            'home-rich-actions',
            '--dry-run'
        )

        [System.IO.File]::WriteAllText($richPreflightPath, $richPreflightOutput, $utf8NoBom)

        Invoke-Native 'node' @(
            '-e',
            $richDryRunValidationScript,
            $richPreflightPath
        )
    }
    finally {
        if (Test-Path -LiteralPath $tempRoot) {
            Remove-Item -LiteralPath $tempRoot -Recurse -Force
        }
    }
}

if ($IncludeAudit) {
    Invoke-Step 'Audit default tool dependency surface' {
        Invoke-Native 'npm' @('audit', '--omit=dev', '--package-lock-only') $ToolRoot
    }
}

Write-Host ''
Write-Host 'All checks passed.'
