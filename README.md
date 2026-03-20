# Markdown Presentation Viewer

A simple, single-page presentation viewer for displaying AI prompts and results in a PPT-like format.

## Quick Start

```bash
python serve.py
```

This will start a local HTTP server on port 8080 and open the presentation in your browser automatically.

## Files

| File | Description |
|------|-------------|
| `presentation.html` | Main HTML file with embedded Markdown renderer |
| `serve.py` | Python HTTP server script (no dependencies) |
| `1_prompt.md` / `1_result.md` | Page 1: Architecture Analysis & Updates |
| `2_prompt.md` / `2_result.md` | Page 2: Business Code Generation |
| `3_prompt.md` / `3_result.md` | Page 3: Development Summary |

## Usage

### Navigation

| Action | Control |
|--------|---------|
| Previous page | `←` key or **Prev** button |
| Next page | `→` key or **Next** button |
| View prompt | `P` key or **Prompt** button |
| View result | `R` key or **Result** button |

### Customizing Content

Edit the corresponding `*_prompt.md` and `*_result.md` files to change the content for each page.

The HTML file has two modes:
- **Server Mode**: Loads content from external `.md` files (when served via HTTP)
- **Inline Mode**: Uses embedded content (when opened directly via `file://`)

## Requirements

- Python 3.x (for `serve.py`)
- Modern web browser with JavaScript enabled

## License

MIT
