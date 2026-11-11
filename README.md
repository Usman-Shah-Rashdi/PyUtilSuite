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

Tagged releases publish downloadable packages to the GitHub Releases page:

- Windows portable ZIP: `File-Utility-Suite-<version>-windows-x64.zip`
- Debian package for x86_64: `file-utility-suite_<version>_amd64.deb`
- RPM package for x86_64: `file-utility-suite-<version>-1.x86_64.rpm`
- Linux AppImage for x86_64: `File-Utility-Suite-<version>-x86_64.AppImage`

Download the appropriate asset from the latest release. The AppImage can be run without installation:

### Install directly from the terminal

Set `VERSION` to the release version you want to install, without the `v` prefix:

```bash
VERSION=1.0
```

Debian and Ubuntu:

```bash
curl -fL -o "file-utility-suite_${VERSION}_amd64.deb" \
  "https://github.com/Usman-Shah-Rashdi/PyUtilSuite/releases/download/v${VERSION}/file-utility-suite_${VERSION}_amd64.deb"
sudo apt install "./file-utility-suite_${VERSION}_amd64.deb"
```

Fedora, RHEL, and openSUSE:

```bash
curl -fL -o "file-utility-suite-${VERSION}-1.x86_64.rpm" \
  "https://github.com/Usman-Shah-Rashdi/PyUtilSuite/releases/download/v${VERSION}/file-utility-suite-${VERSION}-1.x86_64.rpm"
sudo dnf install "./file-utility-suite-${VERSION}-1.x86_64.rpm"
```

To download and run the AppImage:

```bash
curl -fL -o "File-Utility-Suite-${VERSION}-x86_64.AppImage" \
  "https://github.com/Usman-Shah-Rashdi/PyUtilSuite/releases/download/v${VERSION}/File-Utility-Suite-${VERSION}-x86_64.AppImage"
chmod +x "File-Utility-Suite-${VERSION}-x86_64.AppImage"
./"File-Utility-Suite-${VERSION}-x86_64.AppImage"
```

### Debian and Ubuntu

After downloading the `.deb` package, install it from the terminal with:

```bash
sudo apt install ./file-utility-suite_*.deb
```

### Fedora, RHEL, and openSUSE

After downloading the `.rpm` package, install it from the terminal with:

```bash
sudo dnf install ./file-utility-suite-*.rpm
```

### AppImage

```bash
chmod +x File-Utility-Suite-*.AppImage
./File-Utility-Suite-*.AppImage
```

## Build packaged releases locally

Build the Linux packages on an x86_64 Linux machine:

```bash
sudo apt install python3-tk apt-utils dpkg-dev rpm
chmod +x packaging/linux/*.sh
packaging/linux/build-packages.sh 1.0
```

The output is written to `dist/packages`. If `appimagetool` is installed, an AppImage is produced as well.

Build the Windows portable ZIP from PowerShell:

```powershell
.\packaging\build-windows.ps1 1.0
```

Pushing a tag such as `1.0` runs [`.github/workflows/release.yml`](./.github/workflows/release.yml), builds the Windows and Linux artifacts, and attaches them to a generated GitHub release with release notes. The workflow can also be started manually for a build, but publishing is performed for version tags.

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
