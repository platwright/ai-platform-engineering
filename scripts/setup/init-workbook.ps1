param(
    [string]$Destination = '.'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$root = (Resolve-Path -Path $Destination).Path

$directories = @(
    'progress',
    'my-notes',
    'my-solutions'
)

foreach ($directory in $directories) {
    $path = Join-Path -Path $root -ChildPath $directory
    if (-not (Test-Path -Path $path)) {
        New-Item -Path $path -ItemType Directory | Out-Null
        Write-Host "[CREATED] $directory"
    }
    else {
        Write-Host "[SKIPPED] $directory already exists"
    }
}

$files = @(
    @{ Path = 'progress/README.md'; Content = "# Progress`n`nTrack module-by-module progress here.`n" }
    @{ Path = 'progress/module-00.md'; Content = "# Module 00 Progress`n`n## Starting point`n`n- Current role:`n- Familiar areas:`n- New areas:`n- Why this course:`n" }
    @{ Path = 'my-notes/README.md'; Content = "# My Notes`n`nStore your personal notes, diagrams, and reflections here.`n" }
    @{ Path = 'my-solutions/README.md'; Content = "# My Solutions`n`nStore your challenge answers and lab solutions here.`n" }
)

foreach ($file in $files) {
    $path = Join-Path -Path $root -ChildPath $file.Path
    if (-not (Test-Path -Path $path)) {
        Set-Content -Path $path -Value $file.Content -NoNewline
        Write-Host "[CREATED] $($file.Path)"
    }
    else {
        Write-Host "[SKIPPED] $($file.Path) already exists"
    }
}

Write-Host ''
Write-Host 'Workbook initialization complete.'
exit 0