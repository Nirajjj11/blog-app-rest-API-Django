# Blog API with Django REST Framework

A beginner-friendly yet production-aware Django REST API for managing blog posts, users, authentication, and API documentation. The project demonstrates how to build a clean REST backend with Django, Django REST Framework, custom user models, token/session authentication, and OpenAPI schema generation.

---

## 🚀 Project Overview

This backend application provides a simple blogging platform API where:

- authenticated users can create, read, update, and delete blog posts
- each post is linked to its author
- admin users can manage users through DRF viewsets
- authentication and registration are handled via `dj-rest-auth`
- API documentation is available through DRF Spectacular

It is designed as a learning project, but structured with production-level concerns in mind (environment management, deployment notes, security, database, and API design).

---

## ✅ What the app includes

### Core features

- Django 6 + Django REST Framework API
- Custom user model (`CustomUser`) extending `AbstractUser`
- `Post` model with title, body, author, timestamps
- ViewSet-based API endpoints for posts and users
- Permission control so only authors can edit/delete their posts
- Session + token authentication support
- Registration and auth endpoints via `dj-rest-auth`
- OpenAPI schema and Swagger/Redoc views
- Basic Django test coverage for the post model

### API capabilities

- list all posts and create new blog posts
- fetch, update, and delete individual posts
- user management endpoints
- authentication endpoints for login/logout/password workflows
- interactive API documentation

---

## 🧱 Data models and relationships

### `accounts.CustomUser`

The project uses a custom user model instead of Django's default user.

| Field | Type | Purpose |
|---|---|---|
| `name` | `CharField` | Optional display name for the user |
| inherited `username`, `email`, `password`, `is_active`, etc. | Django auth fields | Standard authentication fields |

This custom model allows the application to evolve without being tied to Django's default user structure.

### `posts.Post`

The main content model for blog articles.

| Field | Type | Purpose |
|---|---|---|
| `title` | `CharField(50)` | Post title |
| `body` | `TextField` | Post content |
| `author` | `ForeignKey` to `AUTH_USER_MODEL` | Links each post to the creating user |
| `created_at` | `DateTimeField(auto_now_add=True)` | Timestamp when the post was created |
| `updated_at` | `DateTimeField(auto_now=True)` | Timestamp when the post was last updated |

### Relationship summary

- One `CustomUser` can create many `Post` rows.
- Each `Post` belongs to exactly one author.
- Deleting a user cascades to their posts (`on_delete=models.CASCADE`).

---

## 🔐 Permissions and API behavior

The project uses a custom DRF permission class:

- `IsAuthorOrReadOnly`
  - authenticated users are allowed to access the API
  - safe methods (`GET`, `HEAD`, `OPTIONS`) are open to authenticated users
  - only the post author can update or delete their own post

The user management API uses `IsAdminUser`, so only admins can manage users.

This creates a simple authorization model that mirrors a real blog backend:

- readers can browse posts
- authors can manage their own content
- admins can manage user accounts

---

## 📁 Folder structure

```text
blog API by book/
├── README.md
├── requirements.txt
├── .venv/                       # local virtual environment
├── django_project/
│   ├── manage.py
│   ├── db.sqlite3               # SQLite database for local development
│   ├── schema.yml               # generated OpenAPI schema
│   ├── accounts/
│   │   ├── models.py            # CustomUser model
│   │   ├── tests.py
│   │   ├── views.py
│   │   ├── forms.py
│   │   ├── apps.py
│   │   └── migrations/
│   ├── posts/
│   │   ├── models.py            # Post model
│   │   ├── serializers.py       # REST serializers
│   │   ├── views.py             # ViewSets and permission handling
│   │   ├── urls.py              # Router-based API routes
│   │   ├── permissions.py       # Custom permissions
│   │   ├── tests.py             # API/model tests
│   │   ├── apps.py
│   │   └── migrations/
│   └── django_project/
│       ├── settings.py          # Django configuration
│       ├── urls.py              # Root routing and docs endpoints
│       ├── wsgi.py
│       └── asgi.py
```

---

## 🛠️ Tech stack

- Python 3.11+
- Django 6.0.5
- Django REST Framework 3.17.1
- `dj-rest-auth` for authentication endpoints
- `django-allauth` for auth integrations
- `drf-spectacular` for schema/documentation
- `django-cors-headers` for CORS support
- SQLite for development (`db.sqlite3`)

---

## 🔧 Setup instructions

### 1. Clone the project

```bash
git clone https://github.com/Nirajjj11/blog-app-rest-API-Django.git
cd "blog API by book"
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

If you are using Git Bash or Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Move into the Django project folder

```bash
cd django_project
```

### 5. Apply migrations

```bash
python manage.py migrate
```

### 6. Create an admin user (optional but recommended)

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

The API will be available at:

- `http://127.0.0.1:8000/`

---

## 📡 API routes

The project uses a router, so the endpoints are grouped under `/api/v1/`.

### Blog posts

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/api/v1/` | List all posts |
| `POST` | `/api/v1/` | Create a post |
| `GET` | `/api/v1/{id}/` | Retrieve a single post |
| `PUT` | `/api/v1/{id}/` | Update a post |
| `PATCH` | `/api/v1/{id}/` | Partially update a post |
| `DELETE` | `/api/v1/{id}/` | Delete a post |

### Users

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/api/v1/users/` | List users |
| `POST` | `/api/v1/users/` | Create a user |
| `GET` | `/api/v1/users/{id}/` | Retrieve a user |
| `PUT` | `/api/v1/users/{id}/` | Update a user |
| `PATCH` | `/api/v1/users/{id}/` | Partial update a user |
| `DELETE` | `/api/v1/users/{id}/` | Delete a user |

### Authentication and docs

| Endpoint | Purpose |
|---|---|
| `/api/v1/dj-rest-auth/login/` | Login and receive auth token |
| `/api/v1/dj-rest-auth/logout/` | Logout and invalidate session/token |
| `/api/v1/dj-rest-auth/registration/` | Register a new account |
| `/api/v1/dj-rest-auth/password/reset/` | Password reset flow |
| `/api/v1/dj-rest-auth/password/change/` | Password change flow |
| `/api/schema/` | OpenAPI schema |
| `/api/schema/swagger-ui/` | Swagger UI |
| `/api/schema/redoc/` | Redoc UI |

---

## 🧪 Example requests

### Login

```bash
curl -X POST http://127.0.0.1:8000/api/v1/dj-rest-auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"demo", "password":"demo123"}'
```

### Create a post

```bash
curl -X POST http://127.0.0.1:8000/api/v1/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"My first post","body":"Hello from the API"}'
```

### List posts

```bash
curl -H "Authorization: Token YOUR_TOKEN" http://127.0.0.1:8000/api/v1/
```

---

## 🧪 Running tests

The current regression coverage checks the blog post model and its author relationship.

```bash
python manage.py test
```

Verified locally with:

```bash
..\.venv\Scripts\python.exe manage.py test posts.tests --verbosity 2
```

Result:

- `Ran 1 test`
- `OK`

---

## 📄 Schema generation

The API schema is generated using `drf_spectacular` and stored in `schema.yml`.

To regenerate the schema:

```bash
python manage.py spectacular --file schema.yml
```

---

## ⚠️ Common complexities and production concerns

This project is simple, but there are a few important concepts to understand:

1. **Custom user model setup**
   - `AUTH_USER_MODEL = "accounts.CustomUser"` must be defined before migrations.
   - changing the user model after data exists is a migration-heavy operation.

2. **Authentication design**
   - the project mixes DRF authentication classes (session + token) and external auth packages.
   - in production, choose a single auth strategy that matches your frontend and security needs.

3. **Database choice**
   - SQLite is fine for local development and demos.
   - production should move to PostgreSQL (or another managed database) for reliability, concurrency, and backup support.

4. **Secrets and environment variables**
   - `SECRET_KEY`, database credentials, and service URLs should never be hardcoded in production.
   - use `.env` files, environment variables, or a secret manager.

5. **Debug and host configuration**
   - `DEBUG=True` and empty `ALLOWED_HOSTS` are development-only settings.
   - production needs `DEBUG=False`, a restricted `ALLOWED_HOSTS`, and secure headers.

6. **Static/media files**
   - use a dedicated static/media storage backend in production (CDN, S3, Azure Blob, etc.).

7. **Email backend**
   - `console.EmailBackend` is useful for development only.
   - production should use SMTP or a transactional email service.

8. **CORS and trusted origins**
   - `CORS_ORIGIN_WHITELIST` and `CSRF_TRUSTED_ORIGINS` are development-oriented settings.
   - production should restrict allowed origins carefully.

9. **Monitoring and logging**
   - add structured logging, request monitoring, and error tracking as traffic grows.

---

## 🚀 Suggested production improvements

For production-grade deployment, consider:

- moving from SQLite to PostgreSQL
- using environment variables for configuration
- enabling HTTPS and secure cookies
- adding rate limiting and throttling
- introducing serializers and validation for stricter input control
- adding full test coverage for views, permissions, and auth flows
- adding pagination and filtering for large datasets
- adding API versioning and better error handling

---

## 🧭 Summary

This repository demonstrates how to build a Django REST API from scratch with:

- custom user models
- relational database models
- REST serializers and viewsets
- permission-based authorization
- auth endpoints
- schema documentation
- local development and production deployment considerations

If you want, this project can be extended into a full production API with PostgreSQL, Docker, JWT auth, image uploads, pagination, and CI/CD.
