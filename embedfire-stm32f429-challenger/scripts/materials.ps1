[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('inventory', 'find', 'list', 'extract')]
    [string]$Action,

    [string]$Root = 'E:\野火【STM32F429开发板-挑战者】资料',
    [string]$Pattern = '.',
    [string]$Archive,
    [string]$EntryPrefix,
    [string]$Destination,
    [switch]$Force
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem

$archiveEncoding = [System.Text.Encoding]::GetEncoding(936)

function Get-FullArchivePath {
    param([Parameter(Mandatory = $true)][string]$ArchiveValue)

    if ([System.IO.Path]::IsPathRooted($ArchiveValue)) {
        $candidate = $ArchiveValue
    }
    else {
        $candidate = Join-Path -Path $Root -ChildPath $ArchiveValue
    }

    if (-not (Test-Path -LiteralPath $candidate -PathType Leaf)) {
        throw "Archive not found: $candidate"
    }

    if ([System.IO.Path]::GetExtension($candidate) -ine '.zip') {
        throw "Only ZIP archives are supported: $candidate"
    }

    return (Resolve-Path -LiteralPath $candidate).Path
}

function Open-ZipReadOnly {
    param([Parameter(Mandatory = $true)][string]$Path)

    return [System.IO.Compression.ZipFile]::Open(
        $Path,
        [System.IO.Compression.ZipArchiveMode]::Read,
        $archiveEncoding
    )
}

if (-not (Test-Path -LiteralPath $Root -PathType Container)) {
    throw "Material root not found: $Root"
}

$rootPath = (Resolve-Path -LiteralPath $Root).Path

switch ($Action) {
    'inventory' {
        $files = @(Get-ChildItem -LiteralPath $rootPath -Recurse -File)
        $totalBytes = ($files | Measure-Object -Property Length -Sum).Sum
        if ($null -eq $totalBytes) {
            $totalBytes = 0
        }

        [pscustomobject]@{ Category = 'summary'; Name = 'Root'; Value = $rootPath }
        [pscustomobject]@{ Category = 'summary'; Name = 'FileCount'; Value = $files.Count }
        [pscustomobject]@{ Category = 'summary'; Name = 'TotalGiB'; Value = [math]::Round($totalBytes / 1GB, 3) }

        $files |
            Group-Object { if ([string]::IsNullOrWhiteSpace($_.Extension)) { '<none>' } else { $_.Extension.ToLowerInvariant() } } |
            Sort-Object Count -Descending |
            ForEach-Object {
                [pscustomobject]@{ Category = 'extension'; Name = $_.Name; Value = $_.Count }
            }

        Get-ChildItem -LiteralPath $rootPath -Directory |
            Sort-Object Name |
            ForEach-Object {
                [pscustomobject]@{ Category = 'directory'; Name = $_.Name; Value = '' }
            }
        break
    }

    'find' {
        try {
            $null = [regex]::new($Pattern)
        }
        catch {
            throw "Invalid regular expression in -Pattern: $Pattern"
        }

        Get-ChildItem -LiteralPath $rootPath -Recurse -File |
            Where-Object { $_.FullName -match $Pattern } |
            ForEach-Object {
                [pscustomobject]@{
                    Source    = 'filesystem'
                    Container = $rootPath
                    Path      = $_.FullName.Substring($rootPath.Length).TrimStart('\')
                    Size      = $_.Length
                }
            }

        $zipFiles = Get-ChildItem -LiteralPath $rootPath -Recurse -File -Filter '*.zip'
        foreach ($zipFile in $zipFiles) {
            $zip = $null
            try {
                $zip = Open-ZipReadOnly -Path $zipFile.FullName
                foreach ($entry in $zip.Entries) {
                    if ($entry.FullName -match $Pattern) {
                        [pscustomobject]@{
                            Source    = 'zip'
                            Container = $zipFile.FullName.Substring($rootPath.Length).TrimStart('\')
                            Path      = $entry.FullName
                            Size      = $entry.Length
                        }
                    }
                }
            }
            catch {
                Write-Warning "Cannot inspect ZIP '$($zipFile.FullName)': $($_.Exception.Message)"
            }
            finally {
                if ($null -ne $zip) {
                    $zip.Dispose()
                }
            }
        }
        break
    }

    'list' {
        if ([string]::IsNullOrWhiteSpace($Archive)) {
            throw '-Archive is required for list.'
        }

        try {
            $null = [regex]::new($Pattern)
        }
        catch {
            throw "Invalid regular expression in -Pattern: $Pattern"
        }

        $archivePath = Get-FullArchivePath -ArchiveValue $Archive
        $zip = Open-ZipReadOnly -Path $archivePath
        try {
            $zip.Entries |
                Where-Object { $_.FullName -match $Pattern } |
                Select-Object @{Name = 'Path'; Expression = { $_.FullName } },
                    @{Name = 'Size'; Expression = { $_.Length } },
                    @{Name = 'CompressedSize'; Expression = { $_.CompressedLength } }
        }
        finally {
            $zip.Dispose()
        }
        break
    }

    'extract' {
        if ([string]::IsNullOrWhiteSpace($Archive)) {
            throw '-Archive is required for extract.'
        }
        if ([string]::IsNullOrWhiteSpace($EntryPrefix)) {
            throw '-EntryPrefix is required for extract.'
        }
        if ([string]::IsNullOrWhiteSpace($Destination)) {
            throw '-Destination is required for extract.'
        }

        $archivePath = Get-FullArchivePath -ArchiveValue $Archive
        $normalizedPrefix = $EntryPrefix.Replace('\', '/').TrimStart('/')
        if (-not $normalizedPrefix.EndsWith('/')) {
            $normalizedPrefix += '/'
        }

        $destinationFull = [System.IO.Path]::GetFullPath($Destination)
        $destinationWithSeparator = $destinationFull.TrimEnd('\', '/') + [System.IO.Path]::DirectorySeparatorChar
        $zip = Open-ZipReadOnly -Path $archivePath

        try {
            $plan = @()
            foreach ($entry in $zip.Entries) {
                if (-not $entry.FullName.StartsWith($normalizedPrefix, [System.StringComparison]::OrdinalIgnoreCase)) {
                    continue
                }

                $relative = $entry.FullName.Substring($normalizedPrefix.Length).TrimStart('/')
                if ([string]::IsNullOrWhiteSpace($relative)) {
                    continue
                }

                $relativeNative = $relative.Replace('/', [System.IO.Path]::DirectorySeparatorChar)
                $outputPath = [System.IO.Path]::GetFullPath((Join-Path -Path $destinationFull -ChildPath $relativeNative))
                if (-not $outputPath.StartsWith($destinationWithSeparator, [System.StringComparison]::OrdinalIgnoreCase)) {
                    throw "Unsafe archive entry path: $($entry.FullName)"
                }

                $isDirectory = $entry.FullName.EndsWith('/') -or [string]::IsNullOrEmpty($entry.Name)
                $plan += [pscustomobject]@{
                    Entry       = $entry
                    OutputPath  = $outputPath
                    IsDirectory = $isDirectory
                }
            }

            if ($plan.Count -eq 0) {
                throw "No entries found below prefix '$EntryPrefix'."
            }

            if (-not $Force) {
                $collisions = @($plan | Where-Object { -not $_.IsDirectory -and (Test-Path -LiteralPath $_.OutputPath) })
                if ($collisions.Count -gt 0) {
                    throw "Extraction would overwrite $($collisions.Count) existing file(s). Choose an empty destination or pass -Force."
                }
            }

            [System.IO.Directory]::CreateDirectory($destinationFull) | Out-Null
            $fileCount = 0
            foreach ($item in $plan) {
                if ($item.IsDirectory) {
                    [System.IO.Directory]::CreateDirectory($item.OutputPath) | Out-Null
                    continue
                }

                $parent = [System.IO.Path]::GetDirectoryName($item.OutputPath)
                [System.IO.Directory]::CreateDirectory($parent) | Out-Null
                [System.IO.Compression.ZipFileExtensions]::ExtractToFile(
                    $item.Entry,
                    $item.OutputPath,
                    $Force.IsPresent
                )
                $fileCount++
            }

            [pscustomobject]@{
                Archive     = $archivePath
                EntryPrefix = $normalizedPrefix
                Destination = $destinationFull
                Files       = $fileCount
            }
        }
        finally {
            $zip.Dispose()
        }
        break
    }
}
