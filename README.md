# Tshirt-Mockup-Generator

**A production-ready Django REST API that generates T-shirt mockups asynchronously.**
Stack: **Django + Django REST Framework + Celery + Redis + Pillow**.
Author: **Zahra Roshani**

---

## ✨ Project Overview

This project provides an API to generate T-shirt mockup images with user-provided text. Image generation is executed asynchronously (Celery + Redis). Each generation request produces mockups for multiple T-shirt base colors (by default 4 colors), and the results are stored and served via Django.

**Key features (completed):**

* Asynchronous background processing via **Celery** and **Redis**.
* Image creation using **Pillow** (supports modern Pillow APIs).
* **Multiple shirt colors** per request (by default: `black`, `blue`, `white`, `yellow`).
* Optional request parameters:

  * `font` (choose a font file name),
  * `text_color` (hex color code),
  * `shirt_color` (array of requested colors).
* API endpoint to start generation (returns `task_id`).
* API endpoint to check task status and get generated images (`results` array with `image_url` and `created_at`).
* API endpoint to list historical mockups with **Pagination** and **Search** (search by `text`).
* Defensive behavior: font fallback, text contrast selection, Pillow 10+ compatible (`textbbox`).
* Clean `requirements.txt` and `.gitignore` for production-ready repo.

---

## 📁 Repo layout (important files)

```
Tshirt-Mockup-Generator/
├── config/
│   ├── settings.py
│   ├── celery.py
│   └── urls.py
├── mockups/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── tasks.py
│   ├── urls.py
│   └── static/mockups/         # base images: black.png blue.png white.png yellow.png
├── media/mockups/              # generated images (gitignored)
├── requirements.txt
├── .gitignore
├── manage.py
└── README.md
```

---

## ⚙️ Prerequisites

* Linux (recommended), macOS or Windows with WSL
* Python 3.10+ (this project used Python 3.12)
* Redis server (local or remote)
* `virtualenv` (recommended)
* Recommended fonts installed (e.g. DejaVu Sans). On Debian/Ubuntu fonts typically live in `/usr/share/fonts/truetype/dejavu/`

---

## 🛠️ Quick setup (local)

1. **Clone repo**

```bash
git clone https://github.com/zarrroshin/Tshirt-Mockup-Generator.git
cd Tshirt-Mockup-Generator
```

2. **Create & activate virtualenv**

```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```


4. **Migrate database**

```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Create media directory**

```bash
mkdir -p media/mockups
```

---

## ▶️ Run services (dev)

**Start Redis** (Linux):

```bash
sudo systemctl start redis-server
# or run redis-server directly
```

**Start Celery worker** (in project root, venv active):

```bash
celery -A config worker -l info
```

**Start Django server second terminal venv active**:

```bash
python manage.py runserver
```

Open API root at: `http://127.0.0.1:8000/`

---

## 📡 API endpoints (complete)

### 1) Generate mockup (async)

**POST** `/api/mockups/generate/`

Request body (JSON):

```json
{
  "text": "Hello World",
  "font": "DejaVuSans-Bold.ttf",      // optional: font file name in fonts folder
  "text_color": "#FFFFFF",            // optional: hex
  "shirt_color": ["white", "black"]   // optional: subset of available colors
}
```

Response:

```json
{
  "task_id": "uuid-string",
  "status": "PENDING",
  "message": "Image generation started."
}
```

* If `shirt_color` is omitted, all default colors are used.
* Font fallback: if `font` not found, a default font (DejaVuSans-Bold) is used.

---

### 2) Get task status and results

**GET** `/api/tasks/{task_id}/`

Response (when succeeded):

```json
{
  "task_id": "uuid-string",
  "status": "SUCCESS",
  "results": [
    {
      "image_url": "http://127.0.0.1:8000/media/mockups/Hello_World_black.png",
      "created_at": "2025-11-03T18:21:19.315402Z"
    },
    {
      "image_url": "http://127.0.0.1:8000/media/mockups/Hello_World_white.png",
      "created_at": "2025-11-03T18:21:19.315402Z"
    }
  ]
}
```

If task is pending/started/failed, `status` will reflect that and `results` will be `null` or omitted.

**Implementation notes**

* The Celery task returns a list of stored image relative URLs.
* The view resolves stored Mockup records in DB (by filename) and returns full absolute URLs and `created_at` timestamps.

---

### 3) Mockup history (list)

**GET** `/api/mockups/`

Supports:

* **Pagination** (PageNumberPagination): `?page=1&page_size=5`
* **Search** (SearchFilter) over the `text` field: `?search=Zahra`

Response example:

```json
{
  "count": 12,
  "next": "http://127.0.0.1:8000/api/v1/mockups/?page=2",
  "previous": null,
  "results": [
    {
      "id": 7,
      "text": "Hello Zahra",
      "image": "http://127.0.0.1:8000/media/mockups/Hello_Zahra_white.png",
      "font": "DejaVuSans-Bold.ttf",
      "text_color": "#FFFFFF",
      "shirt_color": "white",
      "created_at": "2025-11-03T18:21:19.315402Z"
    }
  ]
}
```

---
![Uploading image.png…]()



## 🐳 Optional: Docker (brief)

You can dockerize services:

* A Django container (web).
* A Celery worker container (same image, different entrypoint).
* Redis container.

Example `docker-compose.yml` services: `web`, `worker`, `redis`. Be sure to mount `media/` and `mockups/static/mockups/` into containers.

---






