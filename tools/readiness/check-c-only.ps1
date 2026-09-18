[CmdletBinding()]
param(
    [switch]$RequireLegacyDriveAbsent,
    [switch]$RequireCleanGit
)

$ErrorActionPreference = 'Stop'
$repository = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$results = [ordered]@{}

$legacyDrive = Get-PSDrive -Name 'D' -ErrorAction SilentlyContinue
if ($RequireLegacyDriveAbsent -and $null -ne $legacyDrive) {
    throw 'LEGACY_DRIVE_PRESENT: safely disconnect or unmount D: and rerun with -RequireLegacyDriveAbsent.'
}
$results.legacy_drive_absent = ($null -eq $legacyDrive)

$status = @(git -C $repository status --porcelain=v1)
if ($LASTEXITCODE -ne 0) { throw 'GIT_STATUS_FAILED' }
if ($RequireCleanGit -and $status.Count -ne 0) { throw 'GIT_WORKTREE_NOT_CLEAN' }
$results.git_clean = ($status.Count -eq 0)

$runtimeFiles = @(
    Get-ChildItem (Join-Path $repository 'tools\vpc\source') -Recurse -File
    Get-ChildItem (Join-Path $repository 'tools\vpc\tests') -Recurse -File
    Get-ChildItem (Join-Path $repository 'tools\vpc\profiles') -Recurse -File
    Get-ChildItem (Join-Path $repository 'tools\julia') -Recurse -File -ErrorAction SilentlyContinue
)
$runtimeReferences = @($runtimeFiles | Select-String -Pattern '[Dd]:\\' -SimpleMatch:$false)
if ($runtimeReferences.Count -ne 0) {
    throw ('LEGACY_DRIVE_RUNTIME_REFERENCE: ' + ($runtimeReferences.Path -join ', '))
}
$results.runtime_d_drive_references = 0

$python = 'C:\Program Files\Python310\python.exe'
if (-not (Test-Path -LiteralPath $python -PathType Leaf)) { throw 'PYTHON_NOT_READY_ON_C' }
& $python -c 'import sympy, flint, numpy, scipy, mpmath, z3, cvc5, hypothesis; print("PYTHON_STACK_PASS")'
if ($LASTEXITCODE -ne 0) { throw 'PYTHON_STACK_FAILED' }
& $python -m unittest discover -s (Join-Path $repository 'tools\vpc\tests') -p 'test_*.py' -v
if ($LASTEXITCODE -ne 0) { throw 'VPC_TESTS_FAILED' }
$results.python_stack = 'PASS'
$results.vpc = 'PASS'

$cadabra = Join-Path $env:LOCALAPPDATA 'Programs\Cadabra\cadabra2-cli.exe'
if (-not (Test-Path -LiteralPath $cadabra -PathType Leaf)) { throw 'CADABRA_NOT_READY_ON_C' }
& $cadabra --version
if ($LASTEXITCODE -ne 0) { throw 'CADABRA_LAUNCH_FAILED' }
$results.cadabra = 'PASS'

$julia = Join-Path $env:LOCALAPPDATA 'Programs\Julia-1.12.6\bin\julia.exe'
$juliaProject = Join-Path $repository 'tools\julia'
if (-not (Test-Path -LiteralPath $julia -PathType Leaf)) { throw 'JULIA_NOT_READY_ON_C' }
$env:JULIA_PKG_OFFLINE = 'true'
& $julia --startup-file=no --project=$juliaProject (Join-Path $juliaProject 'smoke.jl')
if ($LASTEXITCODE -ne 0) { throw 'JULIA_ENVIRONMENT_FAILED' }
$results.julia_nemo_ordinarydiffeq = 'PASS'

$lean = Get-Command lean -ErrorAction Stop
$lake = Get-Command lake -ErrorAction Stop
if (-not $lean.Source.StartsWith('C:\', [System.StringComparison]::OrdinalIgnoreCase)) { throw 'LEAN_NOT_ON_C' }
if (-not $lake.Source.StartsWith('C:\', [System.StringComparison]::OrdinalIgnoreCase)) { throw 'LAKE_NOT_ON_C' }
& $lean.Source --version
if ($LASTEXITCODE -ne 0) { throw 'LEAN_LAUNCH_FAILED' }
& $lake.Source --version
if ($LASTEXITCODE -ne 0) { throw 'LAKE_LAUNCH_FAILED' }
$leanFile = Join-Path $env:TEMP ('toe-next-readiness-' + [guid]::NewGuid().ToString('N') + '.lean')
try {
    [System.IO.File]::WriteAllText($leanFile, "example : 1 + 1 = 2 := by decide`n", [System.Text.UTF8Encoding]::new($false))
    & $lean.Source $leanFile
    if ($LASTEXITCODE -ne 0) { throw 'LEAN_COMPILE_FAILED' }
} finally {
    Remove-Item -LiteralPath $leanFile -Force -ErrorAction SilentlyContinue
}
$results.lean_lake = 'PASS'

$results.status = 'PASS'
$results | ConvertTo-Json -Depth 4
