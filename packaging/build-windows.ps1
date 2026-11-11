$ErrorActionPreference = "Stop"
$Version = if ($args.Count -gt 0) { $args[0] } else { "0.1.0" }

python -m pip install -r requirements.txt pyinstaller
python -m PyInstaller --clean --noconfirm file_utility_suite.spec
New-Item -ItemType Directory -Force -Path "dist\packages" | Out-Null
Compress-Archive -Path "dist\file-utility-suite.exe" `
  -DestinationPath "dist\packages\File-Utility-Suite-$Version-windows-x64.zip" `
  -Force
Write-Host "Package written to dist\packages"
