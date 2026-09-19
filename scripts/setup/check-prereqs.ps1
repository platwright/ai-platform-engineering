Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Test-Tool {
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$Names,

        [Parameter(Mandatory = $true)]
        [string]$Label
    )

    foreach ($name in $Names) {
        $command = Get-Command -Name $name -ErrorAction SilentlyContinue
        if ($null -ne $command) {
            Write-Host "[OK] $Label ($($command.Name))"
            return $true
        }
    }

    Write-Host "[MISSING] $Label"
    return $false
}

$checks = @(
    @{ Names = @('git'); Label = 'git' }
    @{ Names = @('python'); Label = 'python' }
    @{ Names = @('uv', 'pip'); Label = 'uv or pip' }
    @{ Names = @('docker'); Label = 'docker' }
    @{ Names = @('kubectl'); Label = 'kubectl' }
    @{ Names = @('kind', 'k3d'); Label = 'kind or k3d' }
    @{ Names = @('helm'); Label = 'helm' }
    @{ Names = @('terraform', 'tofu'); Label = 'terraform or tofu' }
    @{ Names = @('make'); Label = 'make' }
    @{ Names = @('curl'); Label = 'curl' }
    @{ Names = @('jq'); Label = 'jq' }
)

$allPassed = $true

foreach ($check in $checks) {
    if (-not (Test-Tool -Names $check.Names -Label $check.Label)) {
        $allPassed = $false
    }
}

Write-Host ''

if ($allPassed) {
    Write-Host 'Environment check passed.'
    exit 0
}

Write-Host 'Environment check failed. Install the missing required tools and rerun the script.'
exit 1