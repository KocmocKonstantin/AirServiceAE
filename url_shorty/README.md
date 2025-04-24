# URL Shortener Service

A simple URL shortener service built with Django and Django Rest Framework.

## Features

- Shorten long URLs to a 6-character code
- Redirect from shortened URLs to original ones
- Track statistics for each shortened URL
- REST API for programmatic access
- Web interface for manual URL shortening and statistics viewing

## Requirements

- Python 3.11
- Django 4.2+
- Django Rest Framework 3.14+

## Installation

1. Clone the repository:
```
git clone <repository-url>
cd url_shortener
```

2. Create and activate a virtual environment:
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Run migrations:
```
python manage.py migrate
```

5. Create a superuser (optional):
```
python manage.py createsuperuser
```

## Usage

1. Start the development server:
```
python manage.py runserver
```

2. Access the application:
   - Web interface: http://localhost:8000/
   - Statistics page: http://localhost:8000/stats/
   - Admin panel: http://localhost:8000/admin/
   - API: http://localhost:8000/api/

## API Endpoints

- `POST /api/shorten/`: Create a shortened URL
  ```json
  {
    "original_url": "https://example.com/very/long/url"
  }
  ```

- `GET /api/urls/`: List all URLs
- `GET /api/urls/{id}/`: Get details for a specific URL
- `DELETE /api/urls/{id}/`: Delete a URL

## License
