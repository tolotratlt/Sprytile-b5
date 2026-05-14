$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$artifactDir = Join-Path $repoRoot "dist"
$stagingDir = Join-Path $artifactDir "Sprytile"
$zipPath = Join-Path $artifactDir "Sprytile-blender-5.zip"

if (Test-Path $stagingDir) {
    Remove-Item -Recurse -Force $stagingDir
}

if (Test-Path $zipPath) {
    Remove-Item -Force $zipPath
}

New-Item -ItemType Directory -Path $stagingDir -Force | Out-Null

$excludeDirs = @(".git", "__pycache__", "dist")
$excludeFiles = @("*.pyc", "*.pyo")

Get-ChildItem -LiteralPath $repoRoot -Force | Where-Object {
    $excludeDirs -notcontains $_.Name
} | ForEach-Object {
    Copy-Item -LiteralPath $_.FullName -Destination $stagingDir -Recurse -Force -Exclude $excludeFiles
}

Compress-Archive -Path (Join-Path $stagingDir "*") -DestinationPath $zipPath -CompressionLevel Optimal

Write-Output $zipPath
