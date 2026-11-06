param(
    [Parameter(Mandatory=$true)]
    [ValidatePattern('^[a-z0-9][a-z0-9-]{1,61}[a-z0-9]$')]
    [string]$Bucket,
    [string]$ChangesFile
)
$ErrorActionPreference = 'Stop'
$repoPath = Split-Path -Parent $PSScriptRoot
$photos = Get-Content -LiteralPath "$repoPath/src/data/importedPhotos.json" -Raw | ConvertFrom-Json
$projects = Get-Content -LiteralPath "$repoPath/src/data/projects.json" -Raw | ConvertFrom-Json
$objectKeys = @($photos.key) + @($projects.coverKey)
if ($ChangesFile) {
    $changes = Get-Content -LiteralPath $ChangesFile -Raw | ConvertFrom-Json
    foreach ($key in $changes.uploadKeys) {
        if ($key -notin $objectKeys) { throw "Upload key is not in the active manifest: $key" }
    }
    $objectKeys = @($changes.uploadKeys)
}
$objectKeys = @($objectKeys | Sort-Object -Unique)
# Upload only this migration's explicit manifest entries; no bucket settings change.
foreach ($key in $objectKeys) {
    if ($key -notmatch '^(adobe|portfolio)/[a-z0-9-]+/(cover(-[a-f0-9]{20})?|[0-9]{3}|[a-f0-9]{20})\.jpg$') {
        throw "Unexpected object key: $key"
    }
    $filePath = Join-Path $repoPath "public/media/$key"
    if (-not (Test-Path -LiteralPath $filePath -PathType Leaf)) {
        throw "Missing local image: $key"
    }
}
$results = $objectKeys | ForEach-Object -Parallel {
    $key = $_
    $filePath = Join-Path $using:repoPath "public/media/$key"
    $bucketName = $using:Bucket
    $succeeded = $false
    for ($attempt = 1; $attempt -le 3; $attempt++) {
        $output = & npx --yes wrangler@4.158.0 r2 object put "$bucketName/$key" --file $filePath --remote --content-type image/jpeg --cache-control 'public, max-age=86400' 2>&1
        if ($LASTEXITCODE -eq 0) { $succeeded = $true; break }
    }
    if ($succeeded) { Write-Host "Uploaded $key" }
    [pscustomobject]@{ Key = $key; Success = $succeeded }
} -ThrottleLimit 5
$failed = @($results | Where-Object { -not $_.Success })
if ($failed.Count) { throw "R2 uploads failed: $($failed.Key -join ', ')" }
Write-Output "Uploaded $($objectKeys.Count) images. Verify their public URLs before setting PUBLIC_PORTFOLIO_MEDIA_URL."
