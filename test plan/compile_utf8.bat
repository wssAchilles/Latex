@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo 正在编译 thuthesis-example.tex ...
xelatex -synctex=1 -interaction=nonstopmode -file-line-error thuthesis-example.tex
if %errorlevel% neq 0 (
    echo 编译失败!
    pause
    exit /b %errorlevel%
)
echo 编译成功!
pause
