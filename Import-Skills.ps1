[CmdletBinding(SupportsShouldProcess)]
param(
    [Parameter(Mandatory=$true)]
    [ValidateSet('claude','zcode')]
    [string]$Client,
    [string]$Destination,
    [string[]]$Names
)
$ErrorActionPreference = 'Stop'
$sourceRoot = $PSScriptRoot
if (-not $Destination) {
    $clientFolder = if ($Client -eq 'claude') { '.claude' } else { '.zcode' }
    $Destination = Join-Path (Join-Path $env:USERPROFILE $clientFolder) 'skills'
}
$destinationRoot = [IO.Path]::GetFullPath($Destination)
if ($destinationRoot.TrimEnd('\','/') -eq [IO.Path]::GetFullPath($sourceRoot).TrimEnd('\','/')) {
    throw 'The destination cannot be the export source directory.'
}
$skillDirectories = @(Get-ChildItem -LiteralPath $sourceRoot -Directory | Where-Object {
    Test-Path -LiteralPath (Join-Path $_.FullName 'SKILL.md') -PathType Leaf
})
if ($Names) {
    $unknown = @($Names | Where-Object { $_ -notin $skillDirectories.Name })
    if ($unknown.Count) { throw "Unknown skills: $($unknown -join ', ')" }
    $skillDirectories = @($skillDirectories | Where-Object { $_.Name -in $Names })
}
$copied = 0
$skipped = 0
foreach ($skillDirectory in $skillDirectories) {
    $target = Join-Path $destinationRoot $skillDirectory.Name
    if (Test-Path -LiteralPath $target) {
        Write-Warning "Already exists; kept unchanged: $target"
        $skipped++
        continue
    }
    if ($PSCmdlet.ShouldProcess($target, 'Copy complete skill directory')) {
        if (-not (Test-Path -LiteralPath $destinationRoot)) {
            New-Item -ItemType Directory -Path $destinationRoot -Force | Out-Null
        }
        Copy-Item -LiteralPath $skillDirectory.FullName -Destination $target -Recurse
        $copied++
    }
}
Write-Output "Client: $Client; copied: $copied; existing skipped: $skipped; selected: $($skillDirectories.Count)"
Write-Output "Destination: $destinationRoot"
if ($Client -eq 'zcode') { Write-Output 'Refresh Settings > Skills in ZCode, then enable the skills you need.' }
else { Write-Output 'Start a new Claude Code session and verify the skills in the / menu.' }
