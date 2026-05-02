# 🚀 Telegraph-Next

[![PyPI](https://img.shields.io/pypi/v/telegraph-next.svg)](https://pypi.org/project/telegraph-next)
[![License](https://img.shields.io/github/license/Abbasxan/telegraph-next.svg)](https://github.com/Abbasxan/telegraph-next/blob/master/LICENSE)

**Telegraph-Next** — это современная, высокопроизводительная асинхронная библиотека для работы с [Telegra.ph API](https://telegra.ph/api), построенная на базе **Pydantic v1** и **aiohttp**.

Это оживленный и улучшенный форк проекта `telegraph_api`, адаптированный для современных высоконагруженных систем и ботов.

## ✨ Ключевые особенности

*   **⚡ Async-first**: Полностью асинхронная архитектура для максимальной скорости.
*   **🛡️ Pydantic Models**: Строгая валидация данных и удобные подсказки в IDE.
*   **🎥 Smart Middlewares**: Автоматическая обработка YouTube-ссылок и очистка HTML.
*   **🧼 Clean Code**: Исправлены критические баги оригинального репозитория (включая загрузку файлов и трансформацию тегов).
*   **🚀 Готовность к нагрузкам**: Оптимизировано для ботов с миллионной аудиторией.

## 📦 Установка

```bash
pip install telegraph-next
```

## Documentation

You can read documentation of this package on [readthedocs](https://telegraph-api.readthedocs.io/en/latest/index.html)

Documentation of original REST api can be found on [telegra.ph](https://telegra.ph/api) site

## Features
- Asynchronous 
- HTML2Nodes convertation
- File uploading
- Built with Pydantic
- Documentation is provided
## 🛠 Использование

```python
import asyncio
from telegraph import Telegraph

# Обязательно используем асинхронную функцию
async def main():
    # Создаем объект библиотеки
    telegraph = Telegraph()
    
    # Создаем новый аккаунт
    await telegraph.create_account(short_name="NeonRobot", author_name="Abbasxan")
    
    # Создаем страницу
    new_page = await telegraph.create_page(
        "My first Telegraph Post",
        content_html="<p>Hello world!</p>" # Поддерживается HTML разметка
    )
    
    # Ссылка на готовую страницу
    print(f"Страница создана: {new_page.url}")

# Запуск асинхронного кода
if __name__ == '__main__':
    asyncio.run(main())
```

## 🚀 Особенности
- **Asynchronous**: Полностью асинхронная работа (требует `await`).
- **HTML2Nodes**: Встроенная конвертация HTML в формат Telegraph.
- **File uploading**: Загрузка медиафайлов одной командой.
- **Pydantic**: Валидация всех данных через модели.

## 📝 Изменения по сравнению с оригиналом
*   Исправлен баг парсинга YouTube ID в мидлварях.
*   Добавлены недостающие импорты BeautifulSoup.
*   Добавлена поддержка контекстного менеджера для сессий.
*   Исправлены утечки памяти при загрузке файлов.

## 🤝 Авторство
Оригинальная идея: [IvanProgramming](https://github.com/IvanProgramming)  
Разработка и поддержка форка: [Abbasxan](https://github.com/Abbasxan)

---
Licensed under [MIT](LICENSE).
