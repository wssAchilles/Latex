# Match - LaTeX 报告/论文模板

`Match` 文件夹包含一个基于 TU Delft 格式的 LaTeX 报告/论文模板。它遵循以下三个关键设计原则：

- **简洁优先**：大幅简化的模板文件，便于自定义。
- **即开即用**：精选常用软件包，开箱即用。
- **功能完整**：提供完善的文档和文件结构，支持完整的项目需求。

该模板支持 _pdfLaTeX_、_XeLaTeX_ 和 _LuaLaTeX_。为了完全符合 TU Delft 的风格指南，建议使用 _XeLaTeX_ 或 _LuaLaTeX_，因为它们支持 TrueType 和 OpenType 字体。模板中使用 _BibLaTeX_ 管理参考文献，并以 _biber_ 作为后台支持。

## 文件夹结构

1. **figure**: 包含文档中使用的所有图片和图形。
2. **frontmatter**: 包含标题页和其他前置页面内容。
3. **mainmatter**: 存放文档的主要内容，例如章节和段落。

## 功能特色

- **自动生成封面和标题页**：通过 `\makecover` 命令生成专业风格的封面和标题页，可选择适用于报告或论文的格式。
- **参考文献管理**：在 `report.tex` 中轻松自定义参考文献，参考文献包含在目录中，并重命名为 "References"。
- **模块化文件组织**：章节和附录分为不同的文件和文件夹，方便管理和编辑。

有关详细文档，请访问 [TU Delft 报告文档](https://dzwaneveld.github.io/report/)。

## 许可协议

该模板基于 [Daan Zwaneveld 的 TU Delft 非官方报告模板](https://github.com/dzwaneveld/TU-Delft-Unofficial-Report-Template)，并采用 [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) 许可协议。使用此模板生成的 PDF 输出无需注明出处。

*→ 访问 [完整文档](https://dzwaneveld.github.io/report/) 了解更多详情。*
