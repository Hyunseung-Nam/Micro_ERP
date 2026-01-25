# 항상 프로젝트 루트 기준으로 실행
$PROJECT_ROOT = Split-Path -Parent $PSScriptRoot
Set-Location $PROJECT_ROOT

Write-Host "=== Release build start ==="
Write-Host "Project Root: $PROJECT_ROOT"

# 기존 빌드 폴더 제거
Remove-Item -Recurse -Force dist, build -ErrorAction SilentlyContinue

# release 폴더 정리(선택)
Remove-Item -Recurse -Force release -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force release | Out-Null

# PyInstaller 빌드 (onedir)
pyinstaller --noconsole --onedir `
  --clean `
  --name "ClientPointManager" `
  src\main.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "[FAIL] PyInstaller build failed."
    exit 1
}

# onedir 결과물 폴더 경로
$bundleDir = Join-Path $PROJECT_ROOT "dist\ClientPointManager"
$exePath   = Join-Path $bundleDir "ClientPointManager.exe"

if (-not (Test-Path $bundleDir)) {
    Write-Host "[FAIL] Output folder not found: $bundleDir"
    exit 1
}
if (-not (Test-Path $exePath)) {
    Write-Host "[FAIL] Output exe not found: $exePath"
    exit 1
}

# release에 런타임 번들 전체 복사 (exe + dll + 포함된 파일들)
$releaseDir = Join-Path $PROJECT_ROOT "release\ClientPointManager"
Copy-Item $bundleDir $releaseDir -Recurse -Force

Write-Host "=== Release build complete ==="
Write-Host "Release Folder: $releaseDir"
Write-Host "EXE: $($releaseDir)\ClientPointManager.exe"
