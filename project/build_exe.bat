@echo off
setlocal
cd /d %~dp0\project
python -m PyInstaller --noconfirm --clean --windowed --name "PDFDocumentConverterPro" --add-data "config;config" --add-data "ui/styles;ui/styles" main.py
echo Build completed. Executable is in dist\PDFDocumentConverterPro
