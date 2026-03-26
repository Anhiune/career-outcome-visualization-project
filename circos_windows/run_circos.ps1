param(
    [string]$Config = "major_industry_circos_draft1\portable_example\circos.conf",
    [string]$OutputDir = "",
    [string]$OutputFile = ""
)

$ErrorActionPreference = "Stop"

function Find-Perl {
    $candidates = @(
        $env:CIRCOS_PERL,
        "C:\Strawberry\perl\bin\perl.exe"
    ) | Where-Object { $_ }

    foreach ($candidate in $candidates) {
        if (Test-Path $candidate) {
            return (Resolve-Path $candidate).Path
        }
    }

    $cmd = Get-Command perl -ErrorAction SilentlyContinue
    if ($cmd) {
        return $cmd.Source
    }

    throw "Perl was not found. Install Strawberry Perl or set CIRCOS_PERL."
}

function Find-CircosScript {
    $candidates = @(
        $env:CIRCOS_HOME,
        "C:\Users\hoang\Downloads\circos-0.69-10\circos-0.69-10",
        "C:\circos"
    ) | Where-Object { $_ }

    foreach ($root in $candidates) {
        $script = Join-Path $root "bin\circos"
        if (Test-Path $script) {
            return (Resolve-Path $script).Path
        }
    }

    throw "Circos was not found. Extract Circos and set CIRCOS_HOME to its root folder."
}

$configPath = Resolve-Path $Config
$perl = Find-Perl
$circos = Find-CircosScript
$circosRoot = Split-Path (Split-Path $circos -Parent) -Parent

$configDir = Split-Path $configPath.Path -Parent
$renderConfig = Join-Path $configDir ".rendered.circos.conf"
$configText = Get-Content $configPath.Path -Raw
$configText = $configText.Replace("__CIRCOS_ROOT__", ($circosRoot -replace "\\","/"))
Set-Content -Path $renderConfig -Value $configText -NoNewline

$args = @($circos, "-conf", $renderConfig)

if ($OutputDir) {
    $resolvedOutputDir = Resolve-Path $OutputDir -ErrorAction SilentlyContinue
    if (-not $resolvedOutputDir) {
        New-Item -ItemType Directory -Path $OutputDir | Out-Null
        $resolvedOutputDir = Resolve-Path $OutputDir
    }
    $args += @("-outputdir", $resolvedOutputDir.Path)
} else {
    $args += @("-outputdir", $configDir)
}

if ($OutputFile) {
    $args += @("-outputfile", $OutputFile)
}

Write-Host "Perl:   $perl"
Write-Host "Circos: $circos"
Write-Host "Config: $($configPath.Path)"

& $perl @args
