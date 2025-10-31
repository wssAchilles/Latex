@echo off
chcp 65001
cd /d "%~dp0"
xelatex -interaction=nonstopmode thuthesis-example.tex
bibtex thuthesis-example
xelatex -interaction=nonstopmode thuthesis-example.tex
xelatex -interaction=nonstopmode thuthesis-example.tex
pause
