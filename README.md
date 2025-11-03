# 👕 Tshirt Mockup Generator API

A Django REST Framework + Celery + Redis project that generates custom T-shirt mockup images asynchronously.
Users can send text to the API and receive generated T-shirt images with that text printed on them.

---

## 🚀 Features

* Asynchronous background task processing with **Celery + Redis**
* Text rendering on T-shirt mockup images using **Pillow**
* RESTful API built with **Django REST Framework**
* Task status tracking via unique `task_id`
* Media storage and retrieval of generated images

---

## 🛠️ Tech Stack

* **Python 3**
* **Django 5**
* **Django REST Framework**
* **Celery**
* **Redis**
* **Pillow (PIL)**

---

## 📂 Project Structure

```
Tshirt-Mockup-Generator/
│
├── config/                  # Django project settings
│   ├── settings.py
│   ├── celery.py
│   ├── urls.py
│
├── mockups/                 # Main app
│   ├── tasks.py             # Celery tasks for image generation
│   ├── views.py             # API views
│   ├── models.py
│   ├── serializers.py
│   ├── static/mockups/      # Base T-shirt images
│
├── media/mockups/           # Generated T-shirt images
├── manage.py
└── requirements.txt
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/zarrroshin/Tshirt-Mockup-Generator.git
cd Tshirt-Mockup-Generator
```

### 2️⃣ Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Start Redis Server

Make sure Redis is running locally:

```bash
sudo systemctl start redis-server
```

### 5️⃣ Run Migrations

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

### 6️⃣ Start Celery Worker

In a new terminal (with virtual environment activated):

```bash
celery -A config worker -l info
```

### 7️⃣ Start Django Server

```bash
python3 manage.py runserver
```

---

## 🧠 API Endpoints

### 1️⃣ Generate Mockup

**POST** `/api/mockups/generate/`

```json
{
  "text": "Hello World"
}
```

**Response:**

```json
{
  "task_id": "uuid-string",
  "status": "PENDING",
  "message": "Image generation started..."
}
```

---

### 2️⃣ Check Task Status

**GET** `/api/tasks/{task_id}/`

```json
{
  "task_id": "uuid-string",
  "status": "SUCCESS",
  "result": "/media/mockups/Hello_World.png"
}
```

---

## 🖼️ Example Output

After successful execution, generated images will be stored in:

```
media/mockups/
```

Example:

```
media/mockups/Hello_World.png
```

---

## 🧩 Optional Enhancements

* ✅ Add **Pagination** and **Search** for mockup list
* 🔐 Add **JWT Authentication** with `djangorestframework-simplejwt`
* 📜 Add **Swagger/OpenAPI** documentation
* 🐳 Containerize the project using **Docker**

---

## 💬 Author

**Zahra Roshani**
📧 [Zahraroshani973@gmail.com](mailto:Zahraroshani973@gmail.com)
🔗 [GitHub](https://github.com/zarrroshin) | [LinkedIn](https://www.linkedin.com/in/zahraroshani)

---