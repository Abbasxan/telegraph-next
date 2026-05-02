<div align="center">

# 🚀 Telegraph-Next
### *Modern, High-Performance Asynchronous Telegraph API Wrapper*

<p align="center">
  <img src="https://img.shields.io/pypi/v/telegraph-next?style=for-the-badge&logo=pypi&color=blue" alt="PyPI">
  <img src="https://img.shields.io/github/license/Abbasxan/telegraph-next?style=for-the-badge&logo=github&color=green" alt="License">
  <img src="https://img.shields.io/github/stars/Abbasxan/telegraph-next?style=for-the-badge&logo=github&color=yellow" alt="Stars">
  <img src="https://img.shields.io/badge/Python-3.7+-blue?style=for-the-badge&logo=python" alt="Python">
</p>

---

[Quick Start](#-quick-start) • [Key Features](#-key-features) • [Installation](#-installation) • [Bug Report](https://github.com/Abbasxan/telegraph-next/issues)

</div>

## 🌟 Why Telegraph-Next?

**Telegraph-Next** is a revitalized, async-first wrapper for the Telegra.ph API. We took the robust foundation of the original project and upgraded it for the modern era of high-load Telegram bots and scalable services.

## ✨ Key Features

*   **⚡ Fully Asynchronous**: Built from the ground up on `aiohttp` for non-blocking performance.
*   **🛡️ Pydantic-Powered**: Every response is a validated object. Get full IDE autocompletion and type safety.
*   **🎞️ Smart HTML Middlewares**: Automatic YouTube iframe handling and HTML tag filtering out of the box.
*   **🧼 Clean & Fixed**: Zero resource leaks, fixed YouTube parsing bugs, and restored missing dependencies.
*   **🧩 Easy Integration**: Designed as a drop-in modernization for high-load systems.

---

## 📦 Installation

Install the latest version via pip:

```bash
pip install telegraph-next
```

---

## 🛠 Quick Start

### 1. Basic Usage (Classic)
```python
import asyncio
from telegraph import Telegraph

async def main():
    # Initialize the client
    telegraph = Telegraph()
    
    # Create an account
    await telegraph.create_account(short_name='NeonRobot', author_name='Abbasxan')
    
    # Create a new page with HTML content
    page = await telegraph.create_page(
        title='My First Page',
        content_html='<h1>Hello!</h1><p>Created using <b>Telegraph-Next</b>.</p>'
    )
    
    print(f"Page live at: {page.url}")

asyncio.run(main())
```

### 2. Using Context Manager (Recommended)
```python
async with Telegraph() as tg:
    await tg.create_account(short_name='NeonRobot')
    page = await tg.create_page('Modern Way', content_html='<i>Seamless!</i>')
    print(page.url)
```

---

## 🚀 Advanced: HTML Middlewares
Telegraph-Next automatically processes your HTML to ensure it matches Telegra.ph's strict rules:
*   Converts YouTube links to supported embeds.
*   Strips unsupported attributes while keeping `src` and `href`.
*   Unwraps unsupported tags to preserve content.

---

## 🤝 Credits & Support
Developed and maintained by **Abbasxan** (Neon Group).  
Original concept by *IvanProgramming*.

If you find this project useful, please give it a ⭐ on GitHub!

---
<div align="center">
Licensed under <a href="LICENSE">MIT</a>.
</div>
