# Markdown Server

本地 Markdown 文件浏览器和演示工具。

## 快速开始

```bash
python serve.py
```

启动后自动打开浏览器访问文件浏览器页面。

## 功能

### 1. 文件浏览器 (`browser.html`)
- 浏览本地任意目录
- 只显示 `.md` 文件
- 点击文件实时渲染 Markdown
- 支持快速访问驱动器/常用目录

### 2. 演示模式 (`presentation.html`)
- PPT 风格展示 AI 提示词和结果
- 键盘快捷键导航
- 适合演示和分享

## 文件列表

| 文件 | 说明 |
|------|------|
| `serve.py` | Python HTTP 服务器（无第三方依赖） |
| `browser.html` | Markdown 文件浏览器 |
| `presentation.html` | PPT 风格演示页面 |
| `1_prompt.md` / `1_result.md` | 第1页：架构分析与更新 |
| `2_prompt.md` / `2_result.md` | 第2页：业务代码生成 |
| `3_prompt.md` / `3_result.md` | 第3页：开发内容总结 |

## 导航快捷键

| 操作 | 快捷键 |
|------|--------|
| 上一页 | `←` 或 **Prev** 按钮 |
| 下一页 | `→` 或 **Next** 按钮 |
| 查看 Prompt | `P` 键或 **Prompt** 按钮 |
| 查看 Result | `R` 键或 **Result** 按钮 |

## 系统要求

- Python 3.x
- 现代浏览器（支持 JavaScript）

## 许可证

MIT
