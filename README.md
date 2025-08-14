# Air Service (Django)

Django‑приложение для извлечения данных из авиабилетов (PDF и изображения) и их отображения в списке. Для PDF используется PyMuPDF, для изображений — OpenCV + Tesseract (pytesseract) с улучшенной предобработкой.

## Стек
- Python 3.12
- Django 5
- PyMuPDF (fitz)
- OpenCV (cv2)
- Tesseract OCR (pytesseract)

## Структура проекта
```
Air_Service/
├── venv/                      # Виртуальное окружение (игнорируется гитом)
└── air_service/
    ├── manage.py              # Точка запуска Django команд
    ├── air_service/           # Настройки проекта
    └── parser_ticket/         # Приложение с логикой OCR и парсинга
        ├── templates/parser_ticket/
        │   ├── upload.html
        │   └── list.html
        ├── parser.py          # Парсер извлеченного текста
        └── wrapper_ticket.py  # Извлечение текста (PDF/изображения)
```

## Требования
На Ubuntu/Debian установите Tesseract и русский язык:
```bash
sudo apt update
sudo apt install -y tesseract-ocr tesseract-ocr-rus
```

Активируйте виртуальное окружение (fish):
```bash
source venv/bin/activate.fish
```

Установите зависимости (если нужно):
```bash
pip install Django PyMuPDF opencv-python pytesseract Pillow
```

## Запуск проекта
Все команды выполняются из папки, где лежит `manage.py`:
```bash
# 1) Активировать venv (fish)
source venv/bin/activate.fish

# 2) Перейти в каталог с manage.py
cd air_service

# 3) Миграции
python manage.py makemigrations
python manage.py migrate

# 4) (Опционально) Создать суперпользователя
python manage.py createsuperuser

# 5) Запустить сервер разработки
python manage.py runserver
```


Приложение будет доступно на `http://127.0.0.1:8000/`.
- Главная страница — форма загрузки билета
- Список обработанных билетов — `http://127.0.0.1:8000/list/`
- Админка — `http://127.0.0.1:8000/admin/`

## Частые проблемы
- «manage.py: No such file or directory» — вы запускаете команду не из каталога `air_service/` (где лежит `manage.py`). Перейдите в него.
- «Port is already in use» — порт занят другим процессом. Остановите предыдущий сервер или запустите на другом порту: `python manage.py runserver 8001`.
- Пустой текст с изображений — убедитесь, что установлен Tesseract и язык `tesseract-ocr-rus`.

## Лицензия
Свободное использование в учебных целях.