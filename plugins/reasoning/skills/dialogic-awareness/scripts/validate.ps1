param()
$ErrorActionPreference='Stop'
$root=Split-Path -Parent $PSScriptRoot
python (Join-Path $PSScriptRoot 'operate.py') validate --input (Join-Path $root 'tests/fixture.json')
if($LASTEXITCODE -ne 0){exit $LASTEXITCODE}
'PASS'
