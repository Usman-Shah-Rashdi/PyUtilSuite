# File Utility

A desktop Tkinter utility for converting files and organizing folders. It supports light and dark themes, responsive layouts, rounded cards, activity logging, previewing organization changes, and undoing the last organization operation.

## Features

- Image conversion between PNG, JPG, WEBP, BMP, and ICO
- PDF text extraction
- Combining images into a PDF
- Markdown to HTML conversion
- JSON, CSV, and YAML conversion workflows
- Folder organization by file type
- Recursive organization with category-folder protection
- Preview before moving files
- Undo for the last completed organization operation
- Automatic system light/dark theme detection
- Manual light/dark theme toggle
- Activity log and operation status display

## Requirements

- Python 3.9 or newer
- Tkinter
- Dependencies listed in [`requirements.txt`](./requirements.txt)

Tkinter is included with most Python installations. On Debian or Ubuntu, install it separately if needed:

```bash
sudo apt install python3-tk
```

## Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Run

```bash
python file_utility_suite.py
```

## Install packaged releases

Tagged releases publish a Windows portable ZIP and Linux packages for x86_64. Linux users can choose the universal AppImage or add the signed third-party repository once and then use their normal package manager for installation and updates.

### Debian and Ubuntu (APT)

```bash
curl -fsSL https://usman-shah-rashdi.github.io/PyUtilSuite/repo/repository-key.asc \
  | sudo gpg --dearmor -o /usr/share/keyrings/file-utility-suite.gpg
echo "deb [signed-by=/usr/share/keyrings/file-utility-suite.gpg] https://usman-shah-rashdi.github.io/PyUtilSuite/repo/apt stable main" \
  | sudo tee /etc/apt/sources.list.d/file-utility-suite.list
sudo apt update
sudo apt install file-utility-suite
```

Update later with:

```bash
sudo apt update
sudo apt upgrade
```

### Fedora, RHEL, and openSUSE (DNF/YUM)

```bash
sudo rpm --import https://usman-shah-rashdi.github.io/PyUtilSuite/repo/repository-key.asc
sudo tee /etc/yum.repos.d/file-utility-suite.repo >/dev/null <<'EOF'
[file-utility-suite]
name=File Utility Suite
baseurl=https://usman-shah-rashdi.github.io/PyUtilSuite/repo/rpm
enabled=1
gpgcheck=0
repo_gpgcheck=1
gpgkey=https://usman-shah-rashdi.github.io/PyUtilSuite/repo/repository-key.asc
EOF
sudo dnf install file-utility-suite
```

Update later with:

```bash
sudo dnf upgrade
```

no arch support for now. cant figure how to run workflow with arch 
### Arch Linux

```bash
sudo pacman-key --add <(curl -fsSL https://usman-shah-rashdi.github.io/PyUtilSuite/repo/repository-key.asc)
sudo pacman-key --lsign-key REPLACE_WITH_KEY_FINGERPRINT
echo "[file-utility-suite]" | sudo tee -a /etc/pacman.conf
echo "Server = https://usman-shah-rashdi.github.io/PyUtilSuite/repo/arch/\$arch" \
  | sudo tee -a /etc/pacman.conf
sudo pacman -Syu file-utility-suite
```

Update later with:

```bash
sudo pacman -Syu
```

The Arch repository is intended for x86_64. The repository signing key fingerprint is published with each release; verify it before locally signing the key.

### AppImage

Download the `File-Utility-Suite-<version>-x86_64.AppImage` asset from the GitHub release, then run:

```bash
chmod +x File-Utility-Suite-*.AppImage
./File-Utility-Suite-*.AppImage
```

## Build packaged releases locally

Build the Linux portable and native packages on an x86_64 Linux machine:

```bash
sudo apt install python3-tk apt-utils dpkg-dev rpm createrepo-c
chmod +x packaging/linux/*.sh
packaging/linux/build-packages.sh 0.1.0
```

The output is written to `dist/packages`. If `appimagetool` is installed, an AppImage is produced as well. Arch packages require an Arch Linux environment and can be built with:

```bash
packaging/linux/build-arch-package.sh 0.1.0
```

Build the Windows portable ZIP from PowerShell:

```powershell
.\packaging\build-windows.ps1 0.1.0
```

Pushing a tag such as `v0.1.0` runs `.github/workflows/release.yml`, builds the platform artifacts, publishes signed APT/RPM/pacman repositories to the `gh-pages` branch, and attaches the packages to the GitHub release. Configure the `REPOSITORY_GPG_PRIVATE_KEY` Actions secret before publishing; never commit the private signing key.

## Usage notes

- Use **Preview Changes** before organizing a directory.
- Organization requires confirmation before files are moved.
- **Undo Last Organization** is available until another organization operation replaces the undo history or the application closes.
- Converted files are written beside their source files.
- Existing output files may be replaced by conversion operations.

## Validation

Run the syntax check from the project directory:

```bash
python -m py_compile file_utility_suite.py
```
