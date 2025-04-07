# Code 2 Text
<!-- 
![Screenshot](docs/SCREENSHOT.png) -->

A user-friendly tool to combine code files into organized text documents while ignoring unnecessary files like `node_modules`, 'package.lock'.
# User Guide

## Basic Usage
1. Launch the application
2. Click "Add Files" or "Add Folder"
3. Select output directory
4. Click "Convert"

## Advanced Options
- **Timestamp**: Appends current date/time to output filename
- **Output Location**: Choose where to save the combined file

## Troubleshooting
If the app crashes:
- Ensure you have write permissions in the output directory
- Avoid paths with special characters

## Features
- Simple GUI interface
- Preserves file structure
- Skips common ignored files
- Progress tracking
- Output in same directory

## Download
Get the latest release for your OS:
- [Windows](dist/FileConverterPro.exe)
<!-- - [Mac](dist/FileConverterPro.app)
- [Linux](dist/FileConverterPro) -->

## Building from Source
1. Install Python 3.8+
2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Build with PyInstaller:
   ```bash
   pyinstaller build.spec
   ```

## License
MIT - See [LICENSE](LICENSE)