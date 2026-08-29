# 📝 Async FastAPI Blogging Website

A modern, fully-featured, asynchronous blogging platform built with **FastAPI**, **SQLAlchemy 2.0**, **PostgreSQL (asyncpg)**, and **Alembic**. It features a clean server-rendered UI using **Jinja2** templates, secure JWT-based user authentication, asynchronous password reset mail dispatching, and automated profile image processing.

---

## ✨ Features

### 👤 User Authentication & Accounts
*   **Secure Authentication**: JWT-based security using modern OAuth2 Password Bearer protocols.
*   **Password Hashing**: State-of-the-art secure password hashing powered by `pwdlib` and Argon2.
*   **Profile Picture Management**: Upload/update profile pictures. Images are automatically cropped/resized to `300x300` resolution, oriented using EXIF data, optimized, and saved as JPEGs using **Pillow**.
*   **Password Recovery**: Secure token-based password reset flow. Generates cryptographically secure, hashed tokens with expiry times, sent via background email tasks.
*   **Account Settings**: Change usernames, email addresses, and passwords with robust backend validation checks to prevent duplicates.

### ✍️ Blog Post Management
*   **Full CRUD API & Web Controls**: Create, read, update (PUT/PATCH), and delete posts.
*   **Author Verification**: Strictly verifies post ownership before allowing edits or deletions.
*   **Smart Pagination**: Paginated listing endpoints (`limit` and `skip`) to optimize load times and database queries.
*   **Likes System**: Integrated database-backed post liking feature.

### 🎨 Frontend & User Interface
*   **Server-Rendered Templates**: Interactive templates written in HTML and styled with custom CSS via Jinja2.
*   **Home & Feeds**: Shows the latest posts with user avatars and dynamic pagination indicators.
*   **User Profiles & Posts**: View profile pages containing all posts authored by a specific user.
*   **Error Handling**: Integrated custom error pages (such as `404 Not Found` and `422 Unprocessable Entity`) for a smooth user experience.

---

## 🛠️ Tech Stack & Key Libraries

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Backend Core** | [FastAPI](https://fastapi.tiangolo.com/) | High-performance, async web framework for Python. |
| **Server Engine** | [Uvicorn](https://www.uvicorn.org/) | ASGI web server implementation. |
| **ORM** | [SQLAlchemy 2.0](https://www.sqlalchemy.org/) | Object Relational Mapper with native async support. |
| **Database** | [PostgreSQL](https://www.postgresql.org/) | Advanced open-source relational database. |
| **DB Driver** | [asyncpg](https://github.com/MagicStack/asyncpg) | Fast, asynchronous PostgreSQL client library. |
| **Migrations** | [Alembic](https://alembic.opsource.net/) | Database migration tool. |
| **Auth** | [PyJWT](https://pyjwt.readthedocs.io/) & [pwdlib](https://pwdlib.readthedocs.io/) | JSON Web Tokens & modern password hashing. |
| **Templates** | [Jinja2](https://jinja.palletsprojects.com/) | Modern and designer-friendly templating engine. |
| **Image Processing** | [Pillow (PIL)](https://python-pillow.org/) | Processing, resizing, and optimizing user profile photos. |
| **Email Service** | [aiosmtplib](https://github.com/cole/aiosmtplib) | Asynchronous SMTP client for password recovery. |
| **Testing** | [pytest](https://docs.pytest.org/) | Robust unit testing framework. |

---

## 📂 Project Structure

```text
blogging_website/
├── alembic/                # Database migrations history and configuration
├── routers/                # API route controllers
│   ├── posts.py            # Post endpoints (CRUD, Pagination)
│   └── users.py            # User endpoints (Auth, Profiles, Pictures)
├── static/                 # Static assets (CSS, JS, site manifest, profile pics)
├── templates/              # HTML Jinja2 templates (email & frontend layouts)
├── tests/                  # Test suites (pytest framework)
├── auth.py                 # JWT token generation, verification & auth dependency
├── config.py               # Pydantic Settings models loadable from .env
├── database.py             # SQLAlchemy Async Engine and Session configuration
├── email_utils.py          # Asynchronous mail-sending utilities using aiosmtplib
├── image_utils.py          # Image compression, resizing, and cropping routines
├── main.py                 # FastAPI application root & HTML web page routing
├── model.py                # SQLAlchemy Declarative models (User, Post, ResetToken)
├── schema.py               # Pydantic validation schemas (requests & responses)
├── .env                    # System environment configuration variables
└── requirements.txt        # Python package dependencies
```

---

## ⚙️ Configuration & Environment Variables

Create a `.env` file in the root directory and configure it as follows:

```env
# Security
SECRET_KEY=your_super_secret_hex_string
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
RESET_TOKEN_EXPIRE_MINUTES=60

# Database
DATABASE_URL=postgresql+asyncpg://<username>:<password>@localhost:<port>/<db_name>

# Mail Server Setup (e.g., Mailtrap, Gmail, or local server)
MAIL_SERVER=sandbox.smtp.mailtrap.io
MAIL_PORT=2525
MAIL_USERNAME=your_smtp_username
MAIL_PASSWORD=your_smtp_password
MAIL_FROM=noreply@yourdomain.com
MAIL_USE_TLS=True

# Application URL
FRONTEND_URL=http://localhost:8000
```

---

## 🚀 Installation & Local Setup

Follow these steps to run the project on your local machine:

### 1. Prerequisites
Ensure you have **Python 3.12** installed on your system along with **PostgreSQL**.

### 2. Clone the Repository
```bash
git clone <your-repository-url>
cd blogging_website
```

### 3. Set Up Virtual Environment
On Windows (PowerShell):
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```
On macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Setup Database & Migrations
Ensure your PostgreSQL server is running and the database matches your `DATABASE_URL`. Run the migrations using Alembic:
```bash
alembic upgrade head
```

### 6. Run the Application
Start the Uvicorn development server:
```bash
uvicorn main:app --reload
```
The application will be accessible at: **[http://localhost:8000](http://localhost:8000)**

---

## 🔌 API Endpoints Documentation

FastAPI auto-generates interactive documentation for all API routes.

*   **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs) (Allows direct testing of endpoints)
*   **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Summary of Routes

#### 🔑 Authentication & Users (`/api/users`)
*   `POST /api/users` - Register a new user account.
*   `POST /api/users/token` - Authenticate user & get OAuth2 Bearer token (Login).
*   `GET /api/users/me` - Fetch authenticated user details.
*   `PATCH /api/users/me/password` - Update account password.
*   `POST /api/users/forgot-password` - Request a password reset link.
*   `POST /api/users/reset-password` - Reset password using the emailed token.
*   `GET /api/users/{user_id}` - View public profile.
*   `PATCH /api/users/{user_id}` - Update profile details.
*   `PATCH /api/users/{user_id}/picture` - Upload a profile image (automatically processed and compressed).
*   `DELETE /api/users/{user_id}/picture` - Delete current profile image.
*   `DELETE /api/users/{user_id}` - Permanent account deletion.

#### 📝 Posts (`/api/posts`)
*   `POST /api/posts` - Create a new blog post (Authenticated).
*   `GET /api/posts` - Retrieve paginated feed of all posts.
*   `GET /api/posts/{post_id}` - Retrieve a specific post by ID.
*   `PUT /api/posts/{post_id}` - Fully update a post (Title & Content).
*   `PATCH /api/posts/{post_id}` - Partially update post attributes.
*   `DELETE /api/posts/{post_id}` - Delete post (Post author only).

---

## 🧪 Running Tests

The test suite is structured around `pytest`. Run tests using the following command:
```bash
pytest
```
*(Ensure you have a test database configured in the environment before executing tests, as specified in [test_users.py](file:///e:/codes/AI_ML/Backend/FastApi/blogging_website/tests/test_users.py).)*
