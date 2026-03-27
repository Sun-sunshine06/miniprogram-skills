param(
    [string]$OutputPath = ".tmp/gui-check-host-env.json",
    [string]$AutomatorModulePath = "",
    [string]$ProjectPath = "",
    [string]$CliPath = ""
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (Resolve-Path (Join-Path $ScriptRoot '..')).Path

function Assert-Command {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Name
    )

    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "Missing required command on PATH: $Name"
    }
}

function Invoke-Node {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Script,

        [string[]]$Arguments = @()
    )

    Push-Location $RepoRoot
    try {
        $output = & node -e $Script @Arguments
        $exitCode = $LASTEXITCODE
    }
    finally {
        Pop-Location
    }

    if ($exitCode -ne 0) {
        throw "Node command failed with exit code ${exitCode}"
    }

    return ($output | ForEach-Object { $_.ToString() }) -join [Environment]::NewLine
}

function Resolve-CliPath {
    param(
        [string]$ExplicitCliPath
    )

    if ($ExplicitCliPath) {
        return (Resolve-Path $ExplicitCliPath).Path
    }

    $script = @'
const { resolveDefaultCliPath } = require('./tools/wechat-gui-check/lib/check-helpers')
process.stdout.write(resolveDefaultCliPath() || '')
'@

    return (Invoke-Node -Script $script).Trim()
}

function Resolve-AutomatorPackageJsonPath {
    param(
        [string]$ExplicitPath,
        [string]$ProjectRoot
    )

    if ($ExplicitPath) {
        $candidate = Join-Path (Resolve-Path $ExplicitPath).Path 'miniprogram-automator\package.json'
        if (Test-Path -LiteralPath $candidate) {
            return $candidate
        }
    }

    if ($ProjectRoot) {
        $candidate = Join-Path (Resolve-Path $ProjectRoot).Path 'node_modules\miniprogram-automator\package.json'
        if (Test-Path -LiteralPath $candidate) {
            return $candidate
        }
    }

    $toolCandidate = Join-Path $RepoRoot 'tools\wechat-gui-check\node_modules\miniprogram-automator\package.json'
    if (Test-Path -LiteralPath $toolCandidate) {
        return $toolCandidate
    }

    return ''
}

function Resolve-DevToolsExeInfo {
    param(
        [string]$ResolvedCliPath
    )

    if (-not $ResolvedCliPath) {
        return [pscustomobject]@{
            exePath = ''
            fileVersion = ''
            productVersion = ''
        }
    }

    $cliDirectory = Split-Path -Parent $ResolvedCliPath
    $candidateNames = @(
        '微信开发者工具.exe',
        'wechatdevtools.exe',
        'WeChatDevTools.exe'
    )

    foreach ($candidateName in $candidateNames) {
        $candidatePath = Join-Path $cliDirectory $candidateName
        if (Test-Path -LiteralPath $candidatePath) {
            $versionInfo = (Get-Item -LiteralPath $candidatePath).VersionInfo
            return [pscustomobject]@{
                exePath = $candidatePath
                fileVersion = $versionInfo.FileVersion
                productVersion = $versionInfo.ProductVersion
            }
        }
    }

    return [pscustomobject]@{
        exePath = ''
        fileVersion = ''
        productVersion = ''
    }
}

Assert-Command node

$resolvedCliPath = Resolve-CliPath -ExplicitCliPath $CliPath
$devToolsExeInfo = Resolve-DevToolsExeInfo -ResolvedCliPath $resolvedCliPath
$automatorPackageJsonPath = Resolve-AutomatorPackageJsonPath -ExplicitPath $AutomatorModulePath -ProjectRoot $ProjectPath
$nodeVersion = (Invoke-Node -Script "process.stdout.write(process.version)").Trim()
$computerInfo = Get-ComputerInfo

$automatorVersion = ''
if ($automatorPackageJsonPath) {
    $automatorVersion = (Get-Content $automatorPackageJsonPath | ConvertFrom-Json).version
}

$output = [pscustomobject]@{
    capturedAt = (Get-Date).ToString('s')
    machineName = $env:COMPUTERNAME
    os = [pscustomobject]@{
        name = $computerInfo.OsName
        version = $computerInfo.OsVersion
        buildNumber = $computerInfo.OsBuildNumber
        productName = $computerInfo.WindowsProductName
    }
    node = [pscustomobject]@{
        version = $nodeVersion
    }
    wechatDevTools = [pscustomobject]@{
        cliPath = $resolvedCliPath
        cliExists = [bool]($resolvedCliPath -and (Test-Path -LiteralPath $resolvedCliPath))
        exePath = $devToolsExeInfo.exePath
        fileVersion = $devToolsExeInfo.fileVersion
        productVersion = $devToolsExeInfo.productVersion
    }
    automator = [pscustomobject]@{
        packageJsonPath = $automatorPackageJsonPath
        version = $automatorVersion
    }
    notes = @(
        'Attach this file to collaborator-host forward-test evidence.',
        'If the live run uses a disposable repo copy or an AppID override, record that separately in the run notes.'
    )
}

$resolvedOutputPath = Join-Path $RepoRoot $OutputPath
$outputDirectory = Split-Path -Parent $resolvedOutputPath
if ($outputDirectory) {
    New-Item -ItemType Directory -Path $outputDirectory -Force | Out-Null
}

$utf8NoBom = New-Object System.Text.UTF8Encoding -ArgumentList $false
[System.IO.File]::WriteAllText(
    $resolvedOutputPath,
    ($output | ConvertTo-Json -Depth 6),
    $utf8NoBom
)

Write-Host $resolvedOutputPath
