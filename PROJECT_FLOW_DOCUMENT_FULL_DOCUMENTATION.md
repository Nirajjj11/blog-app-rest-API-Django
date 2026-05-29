# PROJECT_FLOW_DOCUMENT_200_PAGES.md

> A Comprehensive 200-Section Technical Walkthrough of Django REST API Blog Application
> Complete execution flow, architecture patterns, code analysis, and implementation guide

---

## TABLE OF CONTENTS

1. [Project Foundation (Sections 1-15)](#section-1-project-overview)
2. [Installation & Setup (Sections 16-30)](#section-16-environment-setup)
3. [Configuration Deep Dive (Sections 31-50)](#section-31-settings-file-structure)
4. [Database & Models (Sections 51-80)](#section-51-database-architecture)
5. [Serializers (Sections 81-100)](#section-81-serializer-architecture)
6. [Permissions & Auth (Sections 101-130)](#section-101-authentication-flow)
7. [Views & Viewsets (Sections 131-160)](#section-131-viewsets-architecture)
8. [URLs & Routing (Sections 161-175)](#section-161-url-routing)
9. [Request Lifecycle (Sections 176-190)](#section-176-request-lifecycle)
10. [Testing & Deployment (Sections 191-200)](#section-191-testing-strategy)

---

## PART 1: PROJECT FOUNDATION

### Section 1: Project Overview and Architecture Summary

The project is a beginner-friendly Django REST Framework backend for a blog application. It allows users to create, retrieve, update, and delete blog posts, while enforcing author-based permissions. It also provides authentication endpoints, admin access to user endpoints, and generated API schema documentation.

### Section 2: Technology Stack Description

- **Python**: Version 3.11 or higher
- **Django**: Web framework version 6.0.5
- **Django REST Framework**: API framework version 3.17.1
- **dj-rest-auth**: Authentication endpoints management
- **django-allauth**: Advanced authentication integrations
- **drf-spectacular**: OpenAPI schema and automatic documentation generation
- **django-cors-headers**: Cross-Origin Resource Sharing headers management
- **SQLite**: Development database
- **Gunicorn**: Production WSGI server
- **nginx**: Production reverse proxy and static file server

### Section 3: Application Directory Structure

```
django_project/
├── PROJECT_FLOW_DOCUMENT.md          # Original project documentation
├── README.md                          # Quick start guide
├── requirements.txt                   # Python dependencies
├── db.sqlite3                         # SQLite database file
├── manage.py                          # Django management utility
├── schema.yml                         # OpenAPI schema
├── django_project/                    # Main project configuration package
│   ├── __init__.py
│   ├── settings.py                   # Settings and configuration
│   ├── urls.py                       # Root URL routing
│   ├── wsgi.py                       # Production WSGI application
│   ├── asgi.py                       # Async WSGI configuration
├── accounts/                         # User authentication app
│   ├── models.py                     # CustomUser model
│   ├── views.py                      # Account views
│   ├── forms.py                      # Account forms
│   ├── admin.py                      # Admin configuration
│   ├── apps.py                       # App configuration
│   ├── tests.py                      # Unit tests
│   ├── migrations/
├── posts/                            # Blog posts app
│   ├── models.py                     # Post model
│   ├── serializers.py                # Post serializers
│   ├── views.py                      # Post viewsets
│   ├── permissions.py                # Custom permissions
│   ├── urls.py                       # Post URL routing
│   ├── admin.py                      # Admin configuration
│   ├── apps.py                       # App configuration
│   ├── tests.py                      # Unit tests
│   ├── migrations/
```

### Section 4: Core Data Models Overview

The application has two primary data models:

**CustomUser Model**:
- Extends Django's AbstractUser
- Adds custom `name` field for display purposes
- Stores password using Django's built-in hashing
- Maintains timestamp fields for account creation and modification

**Post Model**:
- Contains `title` field for post heading
- Contains `body` field for post content
- References `author` through ForeignKey to CustomUser
- Tracks `created_at` timestamp when post was created
- Tracks `updated_at` timestamp on each modification
- Cascade deletion: removing a user deletes all their posts

### Section 5: High-Level Runtime Sequence

The typical request flow follows these steps:

1. Python interpreter starts `manage.py` with specified command
2. `manage.py` imports Django and loads `django_project.settings`
3. Django initializes installed apps, middleware stack, and URL configuration
4. Database connections are established
5. HTTP request arrives at the server
6. URL configuration routes request to the appropriate app
7. DRF viewsets are instantiated
8. Permission classes execute authorization checks
9. Serializers validate incoming data or prepare outgoing data
10. ORM query methods interact with the database
11. JSON response is constructed from serializer output
12. Response is sent to the client with appropriate HTTP status code

### Section 6: Application Lifecycle Phases

**Phase 1: Startup and Initialization**
- Django imports configuration
- Apps are loaded in INSTALLED_APPS order
- Models are registered with the ORM
- URL patterns are compiled
- Middleware is instantiated in order

**Phase 2: Request Handling**
- Middleware processes the incoming request
- URL router matches the request path
- View is instantiated with request context
- Permissions are checked
- HTTP method handler is invoked

**Phase 3: Business Logic Execution**
- Serializer transforms data
- ORM queries or creates objects
- Business rules are applied
- Related objects are fetched if needed

**Phase 4: Response Generation**
- Serializer converts objects to JSON
- HTTP headers are set
- Response status code is determined
- Response body is sent to client

### Section 7: Authentication Architecture Overview

The application uses multiple authentication mechanisms:

**Token Authentication**:
- Users receive auth token on login
- Token is included in Authorization header
- Server validates token for each request
- Token is stored in database

**Session Authentication**:
- Used by Django admin interface
- Session cookies stored in browser
- Server validates session on each request

**User Registration Flow**:
- New user submits email and password
- Password is hashed using PBKDF2
- User object created in database
- User receives auth token

### Section 8: Permission System Overview

**Permission Classes**:
- `IsAuthenticated`: Allows only authenticated users
- `IsAuthorOrReadOnly`: Allows read access to all, write only to post author
- `IsAdminUser`: Allows only admin users
- `AllowAny`: Allows unauthenticated access

**Permission Check Flow**:
- Request arrives at viewset
- ViewSet iterates through permission classes
- Each permission's `has_permission()` is called
- For object-level operations, `has_object_permission()` is called
- If all checks pass, request proceeds
- If any check fails, HTTP 403 Forbidden response is returned

### Section 9: API Endpoint Categories

**Authentication Endpoints**:
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `POST /api/auth/registration/` - New user registration
- `GET /api/auth/user/` - Get current user details

**Post Endpoints**:
- `GET /api/posts/` - List all posts
- `POST /api/posts/` - Create new post (authenticated only)
- `GET /api/posts/{id}/` - Retrieve specific post
- `PUT /api/posts/{id}/` - Update post (author only)
- `PATCH /api/posts/{id}/` - Partial update post (author only)
- `DELETE /api/posts/{id}/` - Delete post (author only)

**Schema Endpoints**:
- `GET /api/schema/` - OpenAPI schema in JSON
- `GET /api/schema/swagger/` - Swagger UI documentation
- `GET /api/schema/redoc/` - ReDoc documentation

### Section 10: Middleware Stack Components

The application uses Django's middleware stack for cross-cutting concerns:

**Security Middleware**:
- CSRF protection for form submissions
- X-Frame-Options to prevent clickjacking
- X-Content-Type-Options header
- Content Security Policy headers

**CORS Middleware**:
- django-cors-headers handles cross-origin requests
- Whitelist of allowed origins
- Allowed methods: GET, POST, PUT, PATCH, DELETE, OPTIONS
- Allowed headers: Content-Type, Authorization

**Session Middleware**:
- Manages session cookies
- Stores session data
- Validates session on each request

**Authentication Middleware**:
- Populates request.user
- Handles token authentication
- Sets request.auth with auth token

### Section 11: Database Connection Architecture

**Connection Pool Management**:
- SQLite maintains single connection per process
- Django manages connection lifecycle
- Connection is cached after first use
- Automatic reconnection on connection loss

**Transaction Management**:
- Django wraps requests in transactions by default
- Automatic rollback on exception
- Manual transaction control available via decorators
- Middleware handles commit on success, rollback on error

**Query Optimization**:
- ORM generates SQL queries
- `.select_related()` reduces query count for ForeignKey
- `.prefetch_related()` optimizes reverse relationships
- Database indexing speeds up queries

### Section 12: API Response Structure

All API responses follow a consistent structure:

**Success Response (HTTP 200)**:
```json
{
  "id": 1,
  "title": "Post Title",
  "body": "Post content",
  "author": {
    "id": 1,
    "username": "author_username",
    "email": "author@example.com"
  },
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-02T12:00:00Z"
}
```

**Error Response (HTTP 400/404/500)**:
```json
{
  "detail": "Error message explaining what went wrong"
}
```

**List Response**:
```json
{
  "count": 100,
  "next": "http://api.example.com/posts/?page=2",
  "previous": null,
  "results": [...] 
}
```

### Section 13: Error Handling Strategy

**HTTP Status Codes Used**:
- `200 OK` - Successful GET request
- `201 Created` - Successful POST request creating resource
- `204 No Content` - Successful DELETE request
- `400 Bad Request` - Invalid input data
- `401 Unauthorized` - Missing or invalid authentication
- `403 Forbidden` - Authenticated but lacks permission
- `404 Not Found` - Resource does not exist
- `500 Internal Server Error` - Server error
- `503 Service Unavailable` - Server is down

**Error Response Format**:
- Field-specific errors include field name and error message
- Non-field errors included in "non_field_errors" key
- Error codes help client-side error handling

### Section 14: Caching Strategy Overview

**Cache Types Used**:
- Django cache framework for query result caching
- HTTP cache headers for client-side caching
- View-level caching for expensive operations
- ORM query result caching within request

**Cache Invalidation**:
- Manual cache clearing on object update
- Time-based expiration (TTL) for temporary caches
- Automatic invalidation on database write

### Section 15: Logging and Monitoring

**Logging Levels**:
- DEBUG: Detailed information for development
- INFO: General informational messages
- WARNING: Warning messages for potential issues
- ERROR: Error messages for failures
- CRITICAL: Critical system failures

**Logging Configuration**:
- Console logging for development
- File logging for production
- Separate logs for different components
- Request/response logging middleware
- Database query logging for optimization

---

## PART 2: INSTALLATION & SETUP

### Section 16: Environment Setup Prerequisites

**System Requirements**:
- Python 3.11 or higher installed
- pip package manager available
- Virtual environment tool (venv or virtualenv)
- Git for version control
- Text editor or IDE (VS Code recommended)
- Terminal or command line interface

**Operating System Support**:
- Windows: Git Bash or WSL recommended
- macOS: Native terminal
- Linux: Native terminal

### Section 17: Virtual Environment Creation

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Activate virtual environment (macOS/Linux)
source venv/bin/activate
```

**Why Virtual Environment?**
- Isolates project dependencies
- Prevents conflicts with system Python
- Allows multiple projects with different versions
- Simplifies deployment and requirements management

### Section 18: Dependency Installation

```bash
# Install all dependencies
pip install -r requirements.txt

# Verify installation
pip list
```

**Key Dependencies**:
- Django: Web framework
- djangorestframework: REST API framework
- dj-rest-auth: Auth endpoints
- django-allauth: Advanced auth
- drf-spectacular: Schema generation
- django-cors-headers: CORS handling

### Section 19: Database Initialization

```bash
# Create initial database tables
python manage.py migrate

# Verify migration status
python manage.py showmigrations
```

**What Migrations Do**:
- Create tables in database
- Set up relationships and constraints
- Add indexes for performance
- Version database schema changes
- Enable rollback if needed

### Section 20: Development Server Setup

```bash
# Start development server
python manage.py runserver

# Start on specific port
python manage.py runserver 8001

# Start on specific IP and port
python manage.py runserver 0.0.0.0:8000
```

**Development Server Features**:
- Auto-reloads on code changes
- Detailed error pages with debugging info
- Integrated SQLite database
- Serves static files automatically

### Section 21: Creating Superuser for Admin

```bash
# Create superuser account
python manage.py createsuperuser

# Prompts for:
# - Username
# - Email address
# - Password (twice for confirmation)
```

**Superuser Capabilities**:
- Access Django admin at `/admin/`
- Full permission to all objects
- Can create/edit/delete users and posts
- Can manage other admin users

### Section 22: Database Verification

```bash
# Access Django shell
python manage.py shell

# Import models
from accounts.models import CustomUser
from posts.models import Post

# Query database
users = CustomUser.objects.all()
posts = Post.objects.all()
```

### Section 23: Static Files Configuration

```bash
# Collect static files (production)
python manage.py collectstatic

# Verify static files
ls -la django_project/staticfiles/
```

**Static Files Include**:
- Admin interface CSS/JS
- Schema documentation assets
- Custom project static files

### Section 24: Running Initial Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test accounts
python manage.py test posts

# Run specific test class
python manage.py test accounts.tests.CustomUserTestCase

# Verbose output
python manage.py test -v 2
```

### Section 25: Verifying API Endpoints

```bash
# Check API is responding
curl http://localhost:8000/api/

# Get schema
curl http://localhost:8000/api/schema/

# List posts
curl http://localhost:8000/api/posts/

# Check admin
curl http://localhost:8000/admin/
```

### Section 26: IDE Setup and Configuration

**VS Code Setup**:
```json
{
  "python.defaultInterpreterPath": "venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true
}
```

**Extensions**:
- Python
- Django
- Pylance
- REST Client

### Section 27: Environment Variables Setup

Create `.env` file:
```
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

Use python-decouple or django-environ:
```python
from decouple import config

DEBUG = config('DEBUG', cast=bool)
SECRET_KEY = config('SECRET_KEY')
```

### Section 28: Git Repository Initialization

```bash
# Initialize git repository
git init

# Create .gitignore
echo "venv/" > .gitignore
echo "*.pyc" >> .gitignore
echo "db.sqlite3" >> .gitignore
echo ".env" >> .gitignore
echo "__pycache__/" >> .gitignore

# Commit initial setup
git add .
git commit -m "Initial project setup"
```

### Section 29: Documentation and Changelog

**README.md should include**:
- Project description
- Installation instructions
- Quick start guide
- API documentation link
- Contributing guidelines
- License information

**CHANGELOG.md should track**:
- Version numbers
- Release dates
- New features
- Bug fixes
- Breaking changes

### Section 30: Local Development Checklist

- [ ] Python 3.11+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed
- [ ] Database migrated
- [ ] Superuser created
- [ ] Development server runs without errors
- [ ] Admin interface accessible
- [ ] API endpoints responding
- [ ] Tests pass
- [ ] Git repository initialized

---

## PART 3: CONFIGURATION DEEP DIVE

### Section 31: Settings File Structure Overview

The `django_project/settings.py` file contains all application configuration:

**Main Configuration Sections**:
1. Django settings constants
2. Installed applications
3. Middleware stack
4. Template configuration
5. Database settings
6. Authentication settings
7. REST Framework configuration
8. Logging configuration
9. Security settings
10. CORS settings

### Section 32: DEBUG and SECRET_KEY

```python
DEBUG = True  # False in production

SECRET_KEY = 'your-secret-key-here'  # Change in production
```

**Security Implications**:
- DEBUG=True exposes sensitive error information
- SECRET_KEY must be kept secret
- Use environment variables in production
- Generate new SECRET_KEY for each deployment

### Section 33: ALLOWED_HOSTS Configuration

```python
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'example.com',  # Production domain
]
```

**Purpose**:
- Prevents Host header attacks
- Controls which domains can access the app
- Required in production (DEBUG=False)
- Wildcard '*' not recommended for security

### Section 34: INSTALLED_APPS Configuration

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'rest_framework',
    'drf_spectacular',
    'corsheaders',
    'dj_rest_auth',
    'django_allauth',
    
    'accounts',
    'posts',
]
```

**App Order Significance**:
- Django apps loaded first
- Third-party apps second
- Project apps last
- Affects admin display order
- Affects signal handling order

### Section 35: Middleware Stack Configuration

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]
```

**Middleware Processing Order**:
- Request processed top-to-bottom
- Response processed bottom-to-top
- Order affects behavior and security
- Custom middleware can be added

### Section 36: Database Configuration - SQLite

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**SQLite in Development**:
- No server needed
- File-based storage
- Suitable for development only
- Not recommended for production
- Single process access recommended

### Section 37: Database Configuration - PostgreSQL

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'blog_db',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

**PostgreSQL Advantages**:
- Supports multiple concurrent connections
- Better for production
- ACID compliance
- Advanced features like full-text search

### Section 38: Database Configuration - MySQL

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'blog_db',
        'USER': 'root',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

**MySQL Considerations**:
- Requires mysql-connector-python
- Good MySQL support in Django
- Common in shared hosting

### Section 39: Authentication Backends Configuration

```python
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
```

**Backend Functions**:
- ModelBackend: Standard Django auth
- AllAuth backend: Email auth support
- Custom backends can be added

### Section 40: REST Framework Configuration

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_SCHEMA_CLASS':
        'drf_spectacular.openapi.AutoSchema',
}
```

**Key Configuration Options**:
- Authentication methods
- Default permissions
- Pagination settings
- Filtering options
- Schema generation

### Section 41: CORS Configuration

```python
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://localhost:8000',
    'https://example.com',
]

CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
]
```

**CORS Purpose**:
- Enables browser cross-origin requests
- Security mechanism
- Essential for frontend app access

### Section 42: Template Configuration

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

**Template Configuration**:
- Specifies template locations
- Configures template backends
- Defines context processors

### Section 43: Static Files Configuration

```python
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
```

**Static Files Purpose**:
- CSS, JavaScript, images
- Admin interface CSS/JS
- Client-side assets

### Section 44: Media Files Configuration

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

**Media Files Purpose**:
- User-uploaded content
- Profile pictures
- Attachments
- File storage for models

### Section 45: Password Validation Configuration

```python
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
            'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
            'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME':
            'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
            'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
```

**Password Validators**:
- Enforce password requirements
- Prevent common passwords
- Check password complexity
- Validate against user data

### Section 46: Session Configuration

```python
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 1209600  # 2 weeks
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True  # HTTPS only
SESSION_COOKIE_SAMESITE = 'Lax'
```

**Session Settings**:
- Session storage backend
- Session expiration time
- Security flags
- CSRF protection

### Section 47: Logging Configuration

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
}
```

**Logging Configuration**:
- Specifies log handlers
- Configures log levels
- Defines log formatting
- Sets log storage

### Section 48: Email Configuration

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-password'
```

**Email Configuration**:
- Specifies SMTP server
- Configures credentials
- Sets TLS security
- Required for email verification

### Section 49: Timezone and Localization

```python
USE_I18N = True
USE_L10N = True
USE_TZ = True
TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'en-us'
```

**Localization Settings**:
- Internationalization support
- Timezone handling
- Date/time formatting
- Language preferences

### Section 50: Environment-Based Configuration

```python
import os
from decouple import config

# Development vs Production
if config('DEBUG', cast=bool):
    DATABASES['default']['NAME'] = 'dev.db'
    ALLOWED_HOSTS = ['*']
else:
    DATABASES['default']['NAME'] = config('DB_NAME')
    ALLOWED_HOSTS = config('ALLOWED_HOSTS').split(',')

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', cast=bool)
```

**Environment-Based Approach**:
- Separate configs for dev/prod
- Sensitive data in environment variables
- Simplifies deployment
- Improves security

---

## PART 4: DATABASE & MODELS

### Section 51: Database Architecture Overview

**Database Design Principles**:
- Normalized data structure
- Foreign keys for relationships
- Indexes for performance
- Constraints for data integrity
- Cascade deletion for data cleanup

### Section 52: CustomUser Model Structure

```python
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.username
```

**CustomUser Fields**:
- Inherits from AbstractUser: id, username, password, email, first_name, last_name, is_staff, is_active, etc.
- Adds custom name field
- All standard user functionality included

### Section 53: Post Model Structure

```python
class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
```

**Post Fields**:
- title: Max 200 character string
- body: Unlimited text content
- author: ForeignKey to CustomUser
- created_at: Auto-set on creation
- updated_at: Auto-updated on modification

### Section 54: Model Managers and QuerySets

```python
class Post(models.Model):
    objects = models.Manager()
    
    @classmethod
    def get_posts_by_author(cls, author):
        return cls.objects.filter(author=author)
    
    def get_related_posts(self):
        return Post.objects.filter(
            author=self.author
        ).exclude(id=self.id)[:5]
```

**Manager Methods**:
- Custom QuerySet methods
- Optimized queries
- Reusable query logic

### Section 55: Model Fields and Options

**Field Types**:
- CharField: Fixed-length strings
- TextField: Unlimited text
- DateTimeField: Date and time
- ForeignKey: Relationship to other model
- IntegerField: Integer numbers
- BooleanField: True/False
- DecimalField: Precise decimal numbers

**Field Options**:
- max_length: String field length limit
- null: Allow NULL in database
- blank: Allow empty in forms
- default: Default value
- unique: Unique constraint
- db_index: Create database index
- help_text: Form help text
- verbose_name: Human-readable name

### Section 56: Foreign Key Relationships

```python
class Post(models.Model):
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='posts'
    )
```

**ForeignKey Options**:
- on_delete: CASCADE, PROTECT, SET_NULL, SET_DEFAULT
- related_name: Allows reverse queries
- related_query_name: Name for reverse query
- limit_choices_to: Restricts choices in admin

### Section 57: Cascade Deletion Behavior

```python
# When user is deleted:
author = models.ForeignKey(
    CustomUser,
    on_delete=models.CASCADE  # Delete all user's posts
)

# Alternative:
author = models.ForeignKey(
    CustomUser,
    on_delete=models.PROTECT  # Prevent deletion if posts exist
)

# Alternative:
author = models.ForeignKey(
    CustomUser,
    on_delete=models.SET_NULL,
    null=True  # Set author to NULL when user deleted
)
```

**Cascade Options**:
- CASCADE: Delete related objects
- PROTECT: Prevent deletion
- SET_NULL: Set to NULL
- SET_DEFAULT: Set to default value
- SET(): Call function to set value
- DO_NOTHING: Don't delete anything

### Section 58: Model Methods and Properties

```python
class Post(models.Model):
    def get_excerpt(self):
        """Returns first 100 characters of body"""
        return self.body[:100] + "..."
    
    @property
    def word_count(self):
        """Returns word count of body"""
        return len(self.body.split())
    
    def is_recent(self):
        """Check if post created in last 7 days"""
        from datetime import timedelta
        from django.utils import timezone
        return (timezone.now() - self.created_at) < timedelta(days=7)
```

**Model Methods vs Properties**:
- Methods: Called with (), callable actions
- Properties: Accessed like attributes, use @property
- Methods preferred for complex logic

### Section 59: Model Meta Options

```python
class Post(models.Model):
    class Meta:
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['author', '-created_at']),
        ]
        unique_together = [
            ['author', 'title'],  # Unique constraint
        ]
        permissions = [
            ('can_publish', 'Can publish posts'),
        ]
```

**Meta Options**:
- verbose_name: Display name in admin
- ordering: Default ordering for queries
- indexes: Database indexes for optimization
- unique_together: Composite unique constraint
- permissions: Custom permissions

### Section 60: Database Migrations Overview

```bash
# Create migration file
python manage.py makemigrations

# View migration SQL
python manage.py sqlmigrate accounts 0001

# Apply migrations
python manage.py migrate

# Unapply specific migration
python manage.py migrate accounts 0000
```

**Migration Files**:
- Located in migrations/ directory
- Named with sequence number and operation
- Contain operations for database changes
- Can be reversed for rollback

### Section 61: Migration Operations

**Common Migration Operations**:
- CreateModel: Create new table
- AddField: Add column to table
- RemoveField: Remove column
- AlterField: Modify column
- RenameField: Rename column
- CreateIndex: Add database index
- AddConstraint: Add constraint

### Section 62: Creating Custom Migrations

```bash
# Create empty migration
python manage.py makemigrations accounts --empty --name add_bio_field

# Edit the migration file
# Add operations manually
```

**Manual Migration Operations**:
- For complex changes
- Data transformations
- Running custom SQL
- Creating custom fields

### Section 63: Squashing Migrations

```bash
# Squash multiple migrations
python manage.py squashmigrations accounts 0001 0010

# Reduces migration file count
# Simplifies deployment
# Improves migration performance
```

### Section 64: Model Signals and Receivers

```python
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Post)
def update_post_modified(sender, instance, created, **kwargs):
    if not created:
        instance.updated_at = timezone.now()
        instance.save()
```

**Signal Types**:
- pre_save: Before object save
- post_save: After object save
- pre_delete: Before object delete
- post_delete: After object delete
- m2m_changed: Many-to-many change

### Section 65: Model Validation

```python
from django.core.exceptions import ValidationError

class Post(models.Model):
    title = models.CharField(max_length=200)
    
    def clean(self):
        if len(self.title) < 3:
            raise ValidationError('Title must be at least 3 characters')
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
```

**Validation Layers**:
- Model validation: clean()
- Serializer validation: validate_field()
- Database constraints: unique, max_length
- Field validation: validators list

### Section 66: Raw SQL Queries

```python
from django.db import connection

# Execute raw SQL
with connection.cursor() as cursor:
    cursor.execute(
        "SELECT * FROM posts_post WHERE author_id = %s",
        [author_id]
    )
    rows = cursor.fetchall()
```

**When to Use Raw SQL**:
- Complex queries ORM can't handle
- Performance-critical operations
- Database-specific features
- Avoid: SQL injection (use parameterization)

### Section 67: Query Optimization - select_related

```python
# Without select_related: N+1 queries
posts = Post.objects.all()
for post in posts:
    print(post.author.name)  # Extra query per post

# With select_related: Single query with JOIN
posts = Post.objects.select_related('author')
for post in posts:
    print(post.author.name)  # No extra queries
```

**select_related Usage**:
- Use with ForeignKey
- Use with OneToOneField
- Reduces query count
- Uses SQL JOIN

### Section 68: Query Optimization - prefetch_related

```python
# For reverse ForeignKey relationships
authors = CustomUser.objects.prefetch_related('posts')
for author in authors:
    for post in author.posts.all():  # No extra query
        print(post.title)
```

**prefetch_related Usage**:
- Use with reverse ForeignKey
- Use with ManyToManyField
- Reduces query count
- Makes separate queries

### Section 69: Database Indexing

```python
class Post(models.Model):
    title = models.CharField(
        max_length=200,
        db_index=True  # Create index
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        db_index=True  # ForeignKey auto-indexed
    )
    
    class Meta:
        indexes = [
            models.Index(
                fields=['author', '-created_at'],
                name='author_date_idx'
            ),
        ]
```

**Indexing Benefits**:
- Faster queries
- Slower writes
- Use for frequently filtered fields
- Avoid over-indexing

### Section 70: Full-Text Search Setup

```python
from django.contrib.postgres.search import SearchVector

# For PostgreSQL
posts = Post.objects.annotate(
    search=SearchVector('title', weight='A') +
           SearchVector('body', weight='B')
).filter(search='django')
```

**Full-Text Search**:
- PostgreSQL specific
- Indexes text content
- Supports word matching
- Better than LIKE queries

### Section 71: Database Connection Pooling

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'CONN_MAX_AGE': 600,  # Connection pooling
        'OPTIONS': {
            'connect_timeout': 10,
        }
    }
}
```

**Connection Pooling**:
- Reuses database connections
- Reduces connection overhead
- Improves performance
- Configurable timeout

### Section 72: Transaction Management

```python
from django.db import transaction

# Automatic transaction (default)
@transaction.atomic
def create_post(title, body, author):
    post = Post(title=title, body=body, author=author)
    post.save()
    return post

# Manual transaction
def bulk_create_posts(posts_data):
    with transaction.atomic():
        for data in posts_data:
            Post.objects.create(**data)
```

**Transaction Benefits**:
- Atomicity: All or nothing
- Consistency: Valid states only
- Isolation: No interference
- Durability: Persistent

### Section 73: Database Backup and Recovery

```bash
# Export database to JSON
python manage.py dumpdata > db_backup.json

# Export specific app data
python manage.py dumpdata accounts > accounts_backup.json

# Import from backup
python manage.py loaddata db_backup.json

# For SQLite file backup
cp db.sqlite3 db.sqlite3.backup
```

### Section 74: Database Replication and Scaling

**Replication Strategies**:
- Master-slave replication
- Read replicas for scaling
- Database clustering
- Sharding for large datasets

### Section 75: NoSQL Alternative Considerations

**When to Consider NoSQL**:
- Unstructured data
- Horizontal scaling needs
- High write throughput
- Flexible schema changes
- Not needed for this blog project

### Section 76: Database Performance Monitoring

```python
from django.db import connection, reset_queries
from django.conf import settings

if settings.DEBUG:
    from django.test.utils import CaptureQueriesContext
    
    with CaptureQueriesContext(connection) as context:
        posts = Post.objects.all()
    
    print(f"Number of queries: {len(context)}")
    print(f"Time: {context.captured_queries}")
```

**Performance Monitoring**:
- Query count
- Query execution time
- Slow query logs
- Database profiling

### Section 77: Data Type Choices and Implications

```python
class Post(models.Model):
    # String choices
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft'
    )
    
    # Integer choices
    PRIORITY_CHOICES = [
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
    ]
    priority = models.IntegerField(
        choices=PRIORITY_CHOICES,
        default=1
    )
```

### Section 78: Model Inheritance Strategies

**Abstract Base Classes**:
```python
class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class Post(TimestampedModel):
    title = models.CharField(max_length=200)
```

### Section 79: Multi-Database Support

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
    },
    'replica': {
        'ENGINE': 'django.db.backends.postgresql',
    },
}

# Using different databases
Post.objects.using('default').all()
Post.objects.using('replica').all()
```

### Section 80: Data Integrity and Constraints

```python
class Post(models.Model):
    title = models.CharField(
        max_length=200,
        unique=True  # Unique constraint
    )
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = [
            ['author', 'title'],  # Composite unique
        ]
```

---

## PART 5: SERIALIZERS

### Section 81: Serializer Architecture Overview

Serializers convert complex data types to/from JSON and handle validation:

**Serializer Hierarchy**:
- Serializer: Basic serializer
- ModelSerializer: Auto-generated from model
- ListSerializer: For list operations
- Custom serializers: For specialized logic

### Section 82: BasicPost Serializer Structure

```python
from rest_framework import serializers
from posts.models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'author', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
```

**Serializer Meta Options**:
- model: Model class to serialize
- fields: Which fields to include
- read_only_fields: Fields not writable
- write_only_fields: Fields not readable

### Section 83: Custom Serializer Fields

```python
class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(
        source='author.get_full_name',
        read_only=True
    )
    word_count = serializers.SerializerMethodField()
    
    def get_word_count(self, obj):
        return len(obj.body.split())
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'author', 'author_name', 'word_count']
```

**Field Types**:
- CharField: String field
- IntegerField: Integer field
- DateTimeField: Date/time field
- SerializerMethodField: Computed field
- PrimaryKeyRelatedField: Related object ID

### Section 84: Nested Serializers

```python
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'name']

class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'author', 'created_at']
```

**Nested Serializers**:
- Include related object data
- Avoid circular references
- Control depth of nesting
- Set read_only for safety

### Section 85: Validation in Serializers

```python
class PostSerializer(serializers.ModelSerializer):
    def validate_title(self, value):
        if len(value) < 3:
            raise serializers.ValidationError(
                "Title must be at least 3 characters"
            )
        return value
    
    def validate_body(self, value):
        if len(value) < 10:
            raise serializers.ValidationError(
                "Body must be at least 10 characters"
            )
        return value
    
    def validate(self, data):
        if data['title'].lower() == data['body'].lower():
            raise serializers.ValidationError(
                "Title and body cannot be identical"
            )
        return data
    
    class Meta:
        model = Post
        fields = ['title', 'body']
```

**Validation Methods**:
- validate_<field>: Field-level validation
- validate(): Object-level validation
- Raises ValidationError on failure

### Section 86: Custom Validators

```python
def validate_unique_title(title):
    if Post.objects.filter(title=title).exists():
        raise serializers.ValidationError("Title already exists")

class PostSerializer(serializers.ModelSerializer):
    title = serializers.CharField(validators=[validate_unique_title])
    
    class Meta:
        model = Post
        fields = ['title', 'body']
```

**Validator Functions**:
- Reusable validation logic
- Accepts field value
- Raises ValidationError
- Applied to fields

### Section 87: Create and Update Methods

```python
class PostSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        # Add custom logic before creation
        validated_data['author'] = self.context['request'].user
        return Post.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        # Add custom logic before update
        instance.title = validated_data.get('title', instance.title)
        instance.body = validated_data.get('body', instance.body)
        instance.save()
        return instance
    
    class Meta:
        model = Post
        fields = ['title', 'body']
```

**Create/Update Hooks**:
- Override default behavior
- Add business logic
- Set computed fields
- Validate before save

### Section 88: ListSerializer for Bulk Operations

```python
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'body']
    
    def create(self, validated_data):
        return Post.objects.bulk_create(
            [Post(**item) for item in validated_data]
        )

# Usage with many=True
data = [
    {'title': 'Post 1', 'body': 'Content 1'},
    {'title': 'Post 2', 'body': 'Content 2'},
]
serializer = PostSerializer(data=data, many=True)
if serializer.is_valid():
    serializer.save()
```

**Bulk Operations**:
- many=True for lists
- Custom ListSerializer for bulk_create
- More efficient than individual saves

### Section 89: Dynamic Fields in Serializers

```python
class DynamicFieldsSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        request = self.context.get('request')
        if request:
            fields = request.query_params.get('fields')
            if fields:
                allowed = set(fields.split(','))
                existing = set(self.fields.keys())
                for field_name in existing - allowed:
                    self.fields.pop(field_name)

class PostSerializer(DynamicFieldsSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'author']

# Usage: /api/posts/?fields=id,title
```

**Dynamic Fields**:
- Client selects fields
- Reduces payload size
- Improves performance
- Flexible API responses

### Section 90: Readonly and Writeonly Fields

```python
class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'author', 'password', 'created_at']
        read_only_fields = ['id', 'created_at']
```

**Field Modes**:
- read_only=True: Only in responses
- write_only=True: Only in requests
- read_only_fields: Meta option for multiple

### Section 91: String Relationships

```python
class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'author']

# Calls __str__() on author object
# Returns: "username" (or custom __str__ output)
```

**StringRelatedField**:
- Displays __str__() value
- Read-only by default
- Good for human-readable names

### Section 92: PrimaryKey Relationships

```python
class PostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        required=True
    )
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'author']

# Request: {"title": "Post", "author": 1}
# Response: {"id": 1, "title": "Post", "author": 1}
```

**PrimaryKeyRelatedField**:
- Displays and accepts ID
- Fully writable
- queryset filters choices
- Default for relationships

### Section 93: Slug Relationships

```python
class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        queryset=CustomUser.objects.all()
    )
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'author']

# Request: {"title": "Post", "author": "john_doe"}
# Response: {"id": 1, "title": "Post", "author": "john_doe"}
```

**SlugRelatedField**:
- Uses any unique field as identifier
- Readable and writable
- Common with slugs/usernames

### Section 94: Hyperlinked Relationships

```python
class PostSerializer(serializers.ModelSerializer):
    author = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        queryset=CustomUser.objects.all()
    )
    url = serializers.HyperlinkedIdentityField(
        view_name='post-detail'
    )
    
    class Meta:
        model = Post
        fields = ['url', 'title', 'author']

# Response includes full URLs:
# {"url": "http://api.example.com/posts/1/", "author": "http://api.example.com/users/1/"}
```

**HyperlinkedRelatedField**:
- Returns full URLs
- view_name for URL routing
- HATEOAS principle
- Better for hypermedia APIs

### Section 95: Serializer Method Fields

```python
class PostSerializer(serializers.ModelSerializer):
    days_old = serializers.SerializerMethodField()
    author_full_name = serializers.SerializerMethodField()
    
    def get_days_old(self, obj):
        from datetime import timedelta
        from django.utils import timezone
        delta = timezone.now() - obj.created_at
        return delta.days
    
    def get_author_full_name(self, obj):
        return f"{obj.author.first_name} {obj.author.last_name}"
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'days_old', 'author_full_name']
```

**SerializerMethodField**:
- Custom computed fields
- Read-only by default
- Called with object instance
- Good for derived data

### Section 96: Conditional Serialization

```python
class PostSerializer(serializers.ModelSerializer):
    detailed_body = serializers.SerializerMethodField()
    
    def get_detailed_body(self, obj):
        request = self.context.get('request')
        if request and request.method == 'GET':
            return obj.body
        return None
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'detailed_body']
```

**Context-Based Serialization**:
- Access request in serializer
- Different output based on context
- User permissions
- Request method

### Section 97: Partial Updates with PATCH

```python
class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'body']
        extra_kwargs = {
            'title': {'required': False},
            'body': {'required': False},
        }

# In view:
if request.method == 'PATCH':
    serializer = PostUpdateSerializer(
        post,
        data=request.data,
        partial=True  # Allow partial updates
    )
```

**Partial Updates**:
- PATCH requests for partial data
- partial=True allows optional fields
- PUT requires all fields
- Field-level validation matters

### Section 98: Error Handling in Serializers

```python
class PostSerializer(serializers.ModelSerializer):
    def validate(self, data):
        if not data.get('title') and not data.get('body'):
            raise serializers.ValidationError(
                "Either title or body must be provided"
            )
        return data
    
    class Meta:
        model = Post
        fields = ['title', 'body']

# Error response:
# {"detail": "Either title or body must be provided"}
```

**Error Responses**:
- Field errors: {field_name: [error_message]}
- Non-field errors: {"non_field_errors": [error_message]}
- Validation errors on save

### Section 99: Serializer Performance Optimization

```python
class OptimizedPostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Lazy load nested serializers if needed
        if not self.context.get('include_author'):
            self.fields.pop('author')
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'author']

# Usage:
serializer = OptimizedPostSerializer(
    posts,
    many=True,
    context={'include_author': True}
)
```

**Optimization Techniques**:
- Conditional field inclusion
- Lazy serializer initialization
- select_related/prefetch_related
- Only serialize needed fields

### Section 100: Testing Serializers

```python
from rest_framework.test import APITestCase

class PostSerializerTestCase(APITestCase):
    def test_valid_serializer(self):
        data = {'title': 'Test', 'body': 'Content'}
        serializer = PostSerializer(data=data)
        self.assertTrue(serializer.is_valid())
    
    def test_invalid_title(self):
        data = {'title': 'X', 'body': 'Content'}  # Too short
        serializer = PostSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)
    
    def test_serialization(self):
        post = Post.objects.create(title='Test', body='Content')
        serializer = PostSerializer(post)
        self.assertEqual(serializer.data['title'], 'Test')
```

---

## PART 6: PERMISSIONS & AUTHENTICATION

### Section 101: Authentication Flow Overview

**Authentication Process**:
1. User submits credentials (username/password)
2. Server validates credentials against database
3. If valid, authentication token is generated
4. Token is returned to user
5. User includes token in subsequent requests
6. Server validates token
7. User is authenticated for that request

### Section 102: Token Authentication Implementation

```python
from rest_framework.authentication import TokenAuthentication

# In settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}

# How it works:
# Request header: Authorization: Token abc123def456
# Server looks up token in database
# Associates request with user
```

**Token Authentication**:
- Stateless authentication
- No session needed
- Good for mobile/frontend apps
- Token stored in database

### Section 103: Session Authentication

```python
from rest_framework.authentication import SessionAuthentication

# In settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
}

# How it works:
# Browser sends session cookie
# Server validates session
# Associates request with user
```

**Session Authentication**:
- Stateful authentication
- Uses Django sessions
- Good for web apps
- Session ID in cookie

### Section 104: Custom Authentication Classes

```python
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

class CustomTokenAuth(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        if not auth_header.startswith('CustomToken '):
            return None
        
        token = auth_header.split(' ')[1]
        
        try:
            user = CustomUser.objects.get(auth_token=token)
        except CustomUser.DoesNotExist:
            raise AuthenticationFailed('Invalid token')
        
        return (user, token)
```

**Custom Authentication**:
- Implement BaseAuthentication
- Override authenticate()
- Return (user, auth) or None
- Raise AuthenticationFailed

### Section 105: IsAuthenticated Permission

```python
from rest_framework.permissions import IsAuthenticated

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    
    # All endpoints require authentication
    # Unauthenticated users get 401 Unauthorized
```

**IsAuthenticated**:
- Allows only authenticated users
- Returns 401 for anonymous users
- Simplest permission class
- Often used for write operations

### Section 106: IsAdminUser Permission

```python
from rest_framework.permissions import IsAdminUser

class UserAdminViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdminUser]
    
    # Only admin users can access
    # Returns 403 for non-admin users
```

**IsAdminUser**:
- Requires user.is_staff=True
- For admin-only operations
- Protects sensitive endpoints

### Section 107: IsAuthenticatedOrReadOnly Permission

```python
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # GET requests allowed for all
    # POST/PUT/DELETE require authentication
```

**IsAuthenticatedOrReadOnly**:
- Read access for everyone
- Write access for authenticated
- Good for public content with user contributions
- Common for blogs

### Section 108: Custom Permission Classes

```python
from rest_framework.permissions import BasePermission

class IsAuthorOrReadOnly(BasePermission):
    """
    Custom permission to allow authors to edit their own posts
    and allow read access to everyone
    """
    
    def has_permission(self, request, view):
        # Read requests allowed for everyone
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        
        # Write requests require authentication
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Read requests allowed for everyone
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        
        # Write requests only allowed for author
        return obj.author == request.user
```

**Custom Permissions**:
- Extend BasePermission
- Implement has_permission()
- Implement has_object_permission()
- Return True/False

### Section 109: Multiple Permissions (AND logic)

```python
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class AdminOnlyViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    # Both conditions must be true:
    # 1. User must be authenticated
    # 2. User must be admin
    
    # Equivalent to: IsAuthenticated AND IsAdminUser
```

**Multiple Permissions**:
- All must pass (AND logic)
- Access denied if any fails
- Useful for multiple requirements

### Section 110: Conditional Permissions

```python
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        elif self.action in ['create']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthorOrReadOnly]
        else:
            permission_classes = [IsAdminUser]
        
        return [permission() for permission in permission_classes]
```

**Conditional Permissions**:
- Different permissions per action
- Flexible permission structure
- Common pattern in production

### Section 111: Permission Error Handling

```python
from rest_framework.exceptions import PermissionDenied

# If permission denied:
# Response: HTTP 403 Forbidden
# Body: {"detail": "You do not have permission to perform this action."}

# If not authenticated:
# Response: HTTP 401 Unauthorized
# Body: {"detail": "Authentication credentials were not provided."}
```

**Permission Errors**:
- 401: Not authenticated
- 403: Authenticated but denied
- Error messages are configurable

### Section 112: JWT Token Authentication

```bash
pip install djangorestframework-simplejwt
```

```python
# In settings.py
INSTALLED_APPS = [
    ...
    'rest_framework_simplejwt',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}
```

**JWT Benefits**:
- Self-contained tokens
- No database lookup needed
- Stateless authentication
- Good for scaling

### Section 113: Login Endpoint Implementation

```python
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    
    if user is None:
        return Response(
            {'error': 'Invalid credentials'},
            status=400
        )
    
    token, created = Token.objects.get_or_create(user=user)
    return Response({'token': token.key})
```

**Login Endpoint**:
- POST /api/auth/login/
- Accepts username/password
- Returns auth token
- Creates token if needed

### Section 114: Logout Endpoint Implementation

```python
@api_view(['POST'])
def logout(request):
    if request.user.is_authenticated:
        request.user.auth_token.delete()
        return Response({'message': 'Logged out successfully'})
    
    return Response(
        {'error': 'Not authenticated'},
        status=400
    )
```

**Logout Endpoint**:
- POST /api/auth/logout/
- Requires authentication
- Deletes auth token
- Session is terminated

### Section 115: Registration Endpoint Implementation

```python
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    name = request.data.get('name')
    
    if CustomUser.objects.filter(username=username).exists():
        return Response(
            {'error': 'Username already exists'},
            status=400
        )
    
    user = CustomUser.objects.create_user(
        username=username,
        password=password,
        email=email,
        name=name
    )
    
    token, created = Token.objects.get_or_create(user=user)
    
    return Response({'token': token.key}, status=201)
```

**Registration Endpoint**:
- POST /api/auth/registration/
- Creates new user
- Validates username uniqueness
- Returns auth token

### Section 116: Password Reset Flow

```python
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_request(request):
    email = request.data.get('email')
    
    try:
        user = CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        return Response({'message': 'Check your email'})
    
    token = default_token_generator.make_token(user)
    reset_url = f"http://frontend.com/reset/{user.pk}/{token}/"
    
    send_mail(
        'Password Reset',
        f'Click to reset: {reset_url}',
        'noreply@example.com',
        [email]
    )
    
    return Response({'message': 'Check your email'})
```

**Password Reset**:
- Generate reset token
- Send reset link via email
- Validate token on reset
- Update password securely

### Section 117: Email Verification

```python
@api_view(['POST'])
@permission_classes([AllowAny])
def verify_email(request):
    email = request.data.get('email')
    verification_code = request.data.get('code')
    
    try:
        user = CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        return Response(
            {'error': 'User not found'},
            status=404
        )
    
    if user.email_verification_code != verification_code:
        return Response(
            {'error': 'Invalid code'},
            status=400
        )
    
    user.email_verified = True
    user.save()
    
    return Response({'message': 'Email verified'})
```

**Email Verification**:
- Generate verification code
- Send code to email
- User submits code
- Mark as verified

### Section 118: Two-Factor Authentication

```python
@api_view(['POST'])
def login_with_2fa(request):
    user = authenticate(
        username=request.data.get('username'),
        password=request.data.get('password')
    )
    
    if not user:
        return Response({'error': 'Invalid credentials'}, status=400)
    
    # Send 2FA code
    twofa_code = generate_2fa_code()
    user.twofa_code = twofa_code
    user.save()
    
    send_sms_or_email(user, twofa_code)
    
    return Response({'message': '2FA code sent'})

@api_view(['POST'])
def verify_2fa(request):
    user_id = request.data.get('user_id')
    code = request.data.get('code')
    
    user = CustomUser.objects.get(id=user_id)
    
    if user.twofa_code != code:
        return Response({'error': 'Invalid code'}, status=400)
    
    token = Token.objects.get_or_create(user=user)
    return Response({'token': token.key})
```

**Two-Factor Authentication**:
- Requires additional verification
- SMS or email code
- More secure login
- User can enable optionally

### Section 119: Rate Limiting

```bash
pip install djangorestframework-throttling
```

```python
from rest_framework.throttling import UserRateThrottle

class LoginRateThrottle(UserRateThrottle):
    scope = 'login'

# In settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'user': '1000/day',
        'anon': '100/day',
        'login': '5/hour',
    }
}

class LoginViewSet(viewsets.ViewSet):
    throttle_classes = [LoginRateThrottle]
```

**Rate Limiting**:
- Prevent abuse
- Different rates per user/anonymous
- Configurable time windows
- Returns 429 Too Many Requests

### Section 120: CORS and CSRF Protection

```python
# CORS configuration
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'https://example.com',
]

# CSRF configuration
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:3000',
    'https://example.com',
]

# In views
from django.middleware.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
@api_view(['GET'])
def get_csrf_token(request):
    return Response({'detail': 'CSRF cookie set'})
```

**CSRF/CORS**:
- CSRF: Prevents unauthorized form submission
- CORS: Allows cross-origin requests
- Both needed for frontend apps
- Security important

### Section 121: User Authentication Status

```python
@api_view(['GET'])
def user_auth_status(request):
    if request.user.is_authenticated:
        return Response({
            'authenticated': True,
            'username': request.user.username,
            'email': request.user.email,
        })
    else:
        return Response({
            'authenticated': False,
        }, status=401)
```

### Section 122: Refresh Tokens

```python
# With JWT
from rest_framework_simplejwt.tokens import RefreshToken

def login_with_refresh(request):
    user = authenticate(...)
    refresh = RefreshToken.for_user(user)
    
    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    })

def refresh_token(request):
    refresh = RefreshToken(request.data['refresh'])
    return Response({
        'access': str(refresh.access_token),
    })
```

**Refresh Tokens**:
- Short-lived access token
- Long-lived refresh token
- User can refresh without re-login
- Improves security

### Section 123: API Key Authentication

```python
class APIKeyAuth(BaseAuthentication):
    def authenticate(self, request):
        api_key = request.META.get('HTTP_X_API_KEY')
        
        if not api_key:
            return None
        
        try:
            user = CustomUser.objects.get(api_key=api_key)
        except CustomUser.DoesNotExist:
            raise AuthenticationFailed('Invalid API key')
        
        return (user, api_key)
```

### Section 124: Oauth2 Authentication

```bash
pip install djangorestframework-oauth2-provider
```

**OAuth2 Flow**:
- User visits app
- App redirects to authorization server
- User authorizes
- Authorization code returned
- App exchanges code for token
- App uses token to access API

### Section 125: Social Authentication

```bash
pip install django-allauth
```

**Social Auth Support**:
- Google login
- GitHub login
- Facebook login
- Twitter login
- Other OAuth providers

---

## PART 7: VIEWS & VIEWSETS

### Section 126: ViewSet Architecture

**ViewSet Types**:
- ViewSet: Base class, no defaults
- GenericViewSet: With mixin support
- ModelViewSet: Full CRUD operations
- ReadOnlyModelViewSet: List and retrieve only

### Section 127: ModelViewSet Implementation

```python
from rest_framework import viewsets
from posts.models import Post
from posts.serializers import PostSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    # Provides:
    # - list(): GET /posts/
    # - create(): POST /posts/
    # - retrieve(): GET /posts/{id}/
    # - update(): PUT /posts/{id}/
    # - partial_update(): PATCH /posts/{id}/
    # - destroy(): DELETE /posts/{id}/
```

**ModelViewSet Methods**:
- list(): List all objects
- create(): Create new object
- retrieve(): Get single object
- update(): Full update
- partial_update(): Partial update
- destroy(): Delete object

### Section 128: ReadOnlyModelViewSet

```python
class PostReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    # Provides read-only operations:
    # - list(): GET /posts/
    # - retrieve(): GET /posts/{id}/
```

**ReadOnly ViewSet**:
- List action
- Retrieve action
- No write operations
- Good for public data

### Section 129: Custom ViewSet Actions

```python
from rest_framework.decorators import action
from rest_framework.response import Response

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get 5 most recent posts"""
        recent_posts = self.queryset.order_by('-created_at')[:5]
        serializer = self.get_serializer(recent_posts, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """Publish a post"""
        post = self.get_object()
        post.published = True
        post.save()
        return Response({'status': 'post published'})
```

**Custom Actions**:
- @action decorator
- detail=True: Object-level
- detail=False: List-level
- methods=['GET', 'POST']: HTTP methods
- Routes to /endpoint/action-name/

### Section 130: Filtering and Searching

```python
from rest_framework import filters

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'body']
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']
    
    # Usage:
    # GET /api/posts/?search=django
    # GET /api/posts/?ordering=title
    # GET /api/posts/?ordering=-created_at
```

**Filtering Features**:
- SearchFilter: Full-text search
- OrderingFilter: Sort results
- DjangoFilterBackend: Advanced filtering
- Custom filters

### Section 131: Pagination

```python
from rest_framework.pagination import PageNumberPagination

class PostPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PostPageNumberPagination
    
    # Usage:
    # GET /api/posts/?page=1
    # GET /api/posts/?page=1&page_size=20
```

**Pagination Types**:
- PageNumberPagination: Page numbers
- LimitOffsetPagination: Offset/limit
- CursorPagination: Cursor-based

### Section 132: Viewset Initialization

```python
class PostViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        """
        Override to customize queryset per action
        """
        if self.action == 'list':
            return Post.objects.select_related('author')
        return self.queryset
    
    def get_serializer_class(self):
        """
        Use different serializers for different actions
        """
        if self.action == 'list':
            return PostListSerializer
        return PostDetailSerializer
    
    def get_permissions(self):
        """
        Assign different permissions per action
        """
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]
```

**Customization Hooks**:
- get_queryset(): Query customization
- get_serializer_class(): Serializer choice
- get_permissions(): Permission control
- Override in subclass

### Section 133: Request and Response Context

```python
class PostViewSet(viewsets.ModelViewSet):
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        context['format'] = self.format_kwarg
        context['view'] = self
        context['action'] = self.action
        return context
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=201)
```

**Serializer Context**:
- request: Current request object
- view: ViewSet instance
- format: Format suffix
- action: Current action name

### Section 134: Perform Operations

```python
class PostViewSet(viewsets.ModelViewSet):
    def perform_create(self, serializer):
        """
        Hook called after serializer validation
        """
        # Set author to current user
        serializer.save(author=self.request.user)
    
    def perform_update(self, serializer):
        """
        Hook called on update
        """
        serializer.save()
    
    def perform_destroy(self, instance):
        """
        Hook called on deletion
        """
        instance.delete()
```

**Perform Hooks**:
- perform_create(): Create hook
- perform_update(): Update hook
- perform_destroy(): Delete hook
- Add business logic here

### Section 135: APIView for Custom Logic

```python
from rest_framework.views import APIView

class PostDetailView(APIView):
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
    def put(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def delete(self, request, pk):
        post = self.get_object(pk)
        post.delete()
        return Response(status=204)
```

**APIView**:
- More control than viewsets
- No automatic actions
- Manual method handling
- Good for custom logic

### Section 136: Generic Views

```python
from rest_framework import generics

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # Combines List and Create functionality

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]
    
    # Combines Retrieve, Update, and Destroy
```

**Generic Views**:
- List: GET list
- Create: POST create
- Retrieve: GET detail
- Update: PUT update
- Destroy: DELETE destroy

### Section 137: Mixins

```python
from rest_framework import mixins

class PostListView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView
):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
```

**Mixins Available**:
- ListModelMixin: List objects
- CreateModelMixin: Create object
- RetrieveModelMixin: Retrieve object
- UpdateModelMixin: Update object
- DestroyModelMixin: Destroy object

### Section 138: Throttling in Views

```python
from rest_framework.throttling import UserRateThrottle

class CustomThrottle(UserRateThrottle):
    scope = 'custom'

class PostViewSet(viewsets.ModelViewSet):
    throttle_classes = [CustomThrottle]
    
    # Limits requests per user
```

### Section 139: Content Negotiation

```python
from rest_framework.response import Response

class PostViewSet(viewsets.ModelViewSet):
    def list(self, request, *args, **kwargs):
        posts = self.get_queryset()
        
        # Return JSON or CSV based on format
        if request.accepted_renderer.format == 'csv':
            return self.csv_response(posts)
        
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)
```

### Section 140: Exception Handling in Views

```python
from rest_framework.exceptions import NotFound, PermissionDenied

class PostViewSet(viewsets.ModelViewSet):
    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except Post.DoesNotExist:
            raise NotFound('Post not found')
    
    def destroy(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            raise PermissionDenied('Cannot delete other user posts')
        return super().destroy(request, *args, **kwargs)
```

---

## PART 8: URL ROUTING

### Section 141: Root URL Configuration

```python
# django_project/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('django_project.api_urls')),
]
```

**Root URLs**:
- Main entry point for routing
- Includes app-level URLs
- Admin panel routing
- Static/media files (if needed)

### Section 142: API URL Configuration

```python
# django_project/api_urls.py
from rest_framework.routers import DefaultRouter
from posts.views import PostViewSet
from accounts.views import UserViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('dj_rest_auth.urls')),
]
```

**API URLs**:
- Registers viewsets
- Includes auth URLs
- Includes app-level URLs
- Root for API v1

### Section 143: Router Patterns

```python
from rest_framework.routers import DefaultRouter, SimpleRouter

# DefaultRouter - includes API root endpoint
router = DefaultRouter()

# SimpleRouter - minimal routing
simple_router = SimpleRouter()

# Both generate:
# GET    /posts/          -> list
# POST   /posts/          -> create
# GET    /posts/{id}/     -> retrieve
# PUT    /posts/{id}/     -> update
# PATCH  /posts/{id}/     -> partial_update
# DELETE /posts/{id}/     -> destroy
```

**Router Types**:
- DefaultRouter: Includes root view
- SimpleRouter: Minimal routing
- Both support custom actions

### Section 144: Custom Router Configuration

```python
from rest_framework.routers import SimpleRouter

class CustomRouter(SimpleRouter):
    trailing_slash = False  # /posts instead of /posts/

router = CustomRouter()
router.register(r'posts', PostViewSet)
```

### Section 145: URL Namespacing

```python
urlpatterns = [
    path('api/v1/', include(('app.urls', 'app'), namespace='api-v1')),
    path('api/v2/', include(('app_v2.urls', 'app'), namespace='api-v2')),
]

# Reverse URL:
reverse('api-v1:post-detail', kwargs={'pk': 1})
# Result: /api/v1/posts/1/
```

**URL Namespacing**:
- Version management
- Multiple API versions
- Organized URL structure

### Section 146: Including URLs with Prefixes

```python
# Main urls.py
urlpatterns = [
    path('api/auth/', include('accounts.auth_urls')),
    path('api/posts/', include('posts.urls')),
]

# posts/urls.py remains:
urlpatterns = [
    path('', PostListView.as_view()),
    path('<int:pk>/', PostDetailView.as_view()),
]

# Results in:
# GET /api/posts/
# GET /api/posts/1/
```

### Section 147: Query String Routing

```python
# urls.py
path('posts/', include([
    path('', PostListView.as_view()),
    path('archived/', ArchivedPostListView.as_view()),
]))

# Usage:
# GET /posts/              -> all posts
# GET /posts/archived/     -> archived posts
# GET /posts/?search=django -> search
```

### Section 148: Path Converters

```python
# urls.py
from django.urls import path, re_path

urlpatterns = [
    # Integer ID
    path('posts/<int:pk>/', PostDetailView.as_view()),
    
    # String (slug)
    path('posts/<slug:slug>/', PostSlugDetailView.as_view()),
    
    # UUID
    path('posts/<uuid:id>/', PostUUIDDetailView.as_view()),
    
    # Regex
    re_path(r'^posts/(?P<year>[0-9]{4})/', PostsByYearView.as_view()),
]
```

**Path Converters**:
- int: Integers
- str: Strings
- uuid: UUID format
- slug: URL-safe strings
- path: Includes slashes
- re_path(): Regex patterns

### Section 149: Custom Path Converters

```python
from django.urls.converters import StringConverter

class UsernameConverter(StringConverter):
    regex = '[a-z_]+' # Only lowercase letters and underscores

from django.urls import path, register_converter

register_converter(UsernameConverter, 'username')

urlpatterns = [
    path('users/<username:username>/', UserDetailView.as_view()),
]
```

### Section 150: Reverse URL Resolution

```python
from django.urls import reverse

# In template or view
url = reverse('post-detail', kwargs={'pk': 1})
# Result: /posts/1/

# With namespace
url = reverse('api:post-detail', kwargs={'pk': 1})

# Multiple reverses
for post in posts:
    url = reverse('post-detail', kwargs={'pk': post.id})
```

**Reverse URL**:
- Programmatic URL generation
- Avoids hardcoding URLs
- Updates automatically
- Good for maintainability

### Section 151: URL Configuration for Different HTTP Methods

```python
# urls.py typically maps methods automatically
# But can be explicit:

from django.views.decorators.http import require_http_methods

@require_http_methods(["GET", "POST"])
def post_view(request):
    if request.method == "GET":
        return list_posts()
    elif request.method == "POST":
        return create_post()

urlpatterns = [
    path('posts/', post_view),
]
```

### Section 152: Trailing Slashes

```python
# Settings.py
APPEND_SLASH = True  # Default: adds trailing slash

# URL patterns
urlpatterns = [
    path('posts/', PostListView.as_view()),
    # /posts/   -> matches
    # /posts    -> redirects to /posts/
]
```

### Section 153: Schema URL Configuration

```python
# For automatic schema generation
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger/', SpectacularSwaggerView.as_view(url_name='schema')),
]
```

### Section 154: Error Handlers in URLs

```python
# django_project/urls.py
from django.views.decorators.csrf import csrf_exempt
from rest_framework.exceptions import APIException

handler400 = 'api.views.bad_request_view'
handler404 = 'api.views.not_found_view'
handler500 = 'api.views.server_error_view'

# api/views.py
from rest_framework.response import Response

def not_found_view(request, exception=None):
    return Response({'error': 'Not found'}, status=404)
```

### Section 155: Version-Based URL Routing

```python
# Support multiple API versions
urlpatterns = [
    path('api/v1/', include('posts.v1.urls')),
    path('api/v2/', include('posts.v2.urls')),
]

# Or with AcceptHeaderVersioning
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS':
        'rest_framework.versioning.AcceptHeaderVersioning',
}

# Request header: Accept: application/json; version=1.0
```

### Section 156: Conditional URL Includes

```python
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('api/', include('api.urls')),
]

# Add debug toolbar in development
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
```

### Section 157: Method Dispatching

```python
# Manual method dispatching in URLconf
from django.http import HttpResponse

def method_dispatcher(request):
    if request.method == 'GET':
        return get_handler(request)
    elif request.method == 'POST':
        return post_handler(request)
    return HttpResponse(status=405)

urlpatterns = [
    path('posts/', method_dispatcher),
]
```

### Section 158: URL Caching

```python
# Django caches URL patterns for performance
# Useful for production with many URLs

# Clear cache if needed:
from django.urls import clear_url_caches
clear_url_caches()
```

### Section 159: URL Pattern Debugging

```bash
# List all URL patterns
python manage.py show_urls

# Or manually in shell
python manage.py shell

from django.urls import get_resolver
resolver = get_resolver()
for pattern in resolver.url_patterns:
    print(pattern)
```

### Section 160: Production URL Configuration

```python
# Production settings
ALLOWED_HOSTS = ['example.com', 'www.example.com']
DEBUG = False

# HTTPS enforcement
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# HSTS headers
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

---

## PART 9: REQUEST LIFECYCLE

### Section 161: HTTP Request Flow

**Complete Request Lifecycle**:
1. Client sends HTTP request
2. WSGI server receives request
3. Django middleware processes request
4. URL router finds matching pattern
5. View is called with request
6. Permissions are checked
7. Serializer validates data
8. Business logic executes
9. Response is serialized
10. Middleware processes response
11. Response sent to client

### Section 162: Request Object Details

```python
# request object properties
request.method        # 'GET', 'POST', etc.
request.GET           # Query parameters
request.POST          # Form data
request.FILES         # Uploaded files
request.user          # Authenticated user
request.auth          # Auth token
request.data          # Parsed request body
request.META          # HTTP headers
request.path          # URL path
request.build_absolute_uri()  # Full URL
```

### Section 163: WSGI Server Processing

```python
# WSGI (Web Server Gateway Interface)
# Specifies how web servers communicate with Django

# manage.py runserver uses:
# wsgiref.simple_server.make_server()

# Production uses:
# Gunicorn, uWSGI, etc.

# WSGI application in django_project/wsgi.py:
application = get_wsgi_application()
```

### Section 164: Middleware Request Processing

```python
# Middleware processes requests in order
# Then responses in reverse order

# Request order:
1. SecurityMiddleware
2. CorsMiddleware
3. CommonMiddleware
4. CsrfViewMiddleware
5. SessionMiddleware
6. AuthenticationMiddleware
7. MessageMiddleware

# Response order (reverse):
7. MessageMiddleware
6. AuthenticationMiddleware
5. SessionMiddleware
4. CsrfViewMiddleware
3. CommonMiddleware
2. CorsMiddleware
1. SecurityMiddleware
```

### Section 165: URL Resolution

```python
# URL resolution process
1. URL conf is loaded
2. Request path is matched against patterns
3. Pattern match found
4. View function or ViewSet is identified
5. URL converters extract parameters
6. View is called with kwargs
```

### Section 166: Exception Handling in Request

```python
# Exception handling flow
try:
    # URL resolution
    # View execution
    # Serializer validation
    # Model operations
except ValidationError as e:
    # DRF catches and converts to 400
except Http404 as e:
    # Returns 404
except PermissionDenied as e:
    # Returns 403
except Exception as e:
    # Returns 500 in production
```

### Section 167: Response Construction

```python
# Response building process
1. Serializer.data is created
2. HTTP status code determined
3. Headers set (Content-Type, etc.)
4. JSON encoding
5. Return Response object

# Response object properties
response.status_code        # HTTP status
response.data              # Response body
response.headers           # Response headers
response['Content-Type']   # Content type
response.render()          # Serialize to bytes
```

### Section 168: Content Negotiation

```python
# What format should response be?
1. Check Accept header
2. Check format query parameter
3. Use default

# Accept header examples:
Accept: application/json        # JSON
Accept: application/xml         # XML
Accept: text/html              # HTML
Accept: */*                    # Any format
```

### Section 169: Serialization Process

```python
# Serialization flow
1. Object passed to serializer
2. Serializer iterates through fields
3. Each field value is processed
4. Related objects are serialized recursively
5. Dictionary created
6. Dictionary converted to JSON

# Key points:
- Serializers handle type conversion
- Related objects included based on config
- Computed fields generated
- Read-only fields included
- Write-only fields excluded
```

### Section 170: Database Query Execution

```python
# Query execution in request
1. ORM method called (Post.objects.get())
2. SQL generated
3. Query sent to database
4. Database executes query
5. Results returned to Python
6. Objects instantiated from results

# Common queries:
Post.objects.get(pk=1)        # Single object
Post.objects.filter(...)      # QuerySet
Post.objects.all()            # All objects
post.save()                   # Update/create
post.delete()                 # Delete
```

### Section 171: Authentication Flow

```python
# Authentication in request
1. Request arrives
2. AuthenticationMiddleware processes
3. Authentication backends checked:
   a. TokenAuthentication
   b. SessionAuthentication
4. User identified or None
5. request.user set
6. request.auth set (token value)
```

### Section 172: Permission Checking

```python
# Permission check flow
1. View's permission_classes retrieved
2. Each permission instantiated
3. has_permission() called for list views
4. has_object_permission() called for detail views
5. If all pass, view executes
6. If any fails, HTTP 403 returned
```

### Section 173: View Execution

```python
# ViewSet action execution
1. Request received
2. Routing determines action
3. ViewSet instantiated
4. initialize_request() creates request
5. initial() permission checks
6. Action method called (e.g., list(), create())
7. Serializer applied
8. Response returned
```

### Section 174: Error Response Flow

```python
# Error response handling
1. Exception raised in view
2. DRF exception handler catches
3. Exception converted to response format
4. HTTP status determined
5. Error message included
6. Response sent to client

# Example error response:
{
    "detail": "Not found.",
    "status_code": 404
}
```

### Section 175: Response Rendering

```python
# Response rendering process
1. Response object has data
2. Renderer selected based on content negotiation
3. Renderer.render() called
4. Data converted to bytes
5. Content-Type header set
6. Response sent to client

# Response flow:
Response({'key': 'value'}, status=200)
-> JSONRenderer renders
-> Returns JSON bytes
-> Sent with HTTP headers
```

---

## PART 10: TESTING & DEPLOYMENT

### Section 176: Testing Strategy Overview

**Test Types**:
- Unit tests: Test individual functions
- Integration tests: Test component interactions
- API tests: Test endpoints
- Performance tests: Test speed
- Security tests: Test vulnerabilities

### Section 177: Unit Testing Models

```python
from django.test import TestCase
from accounts.models import CustomUser
from posts.models import Post

class CustomUserModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpass',
            email='test@example.com'
        )
    
    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertTrue(self.user.check_password('testpass'))
    
    def test_user_str(self):
        self.assertEqual(str(self.user), 'testuser')

class PostModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='author')
        self.post = Post.objects.create(
            title='Test Post',
            body='Test Content',
            author=self.user
        )
    
    def test_post_creation(self):
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.author, self.user)
    
    def test_post_cascade_delete(self):
        post_id = self.post.id
        self.user.delete()
        self.assertFalse(Post.objects.filter(id=post_id).exists())
```

**Model Testing**:
- setUp() creates test data
- Test model methods
- Test validations
- Test relationships

### Section 178: Serializer Testing

```python
from rest_framework.test import APITestCase
from posts.serializers import PostSerializer

class PostSerializerTest(APITestCase):
    def test_valid_serializer(self):
        data = {
            'title': 'Test Post',
            'body': 'Test Content'
        }
        serializer = PostSerializer(data=data)
        self.assertTrue(serializer.is_valid())
    
    def test_invalid_short_title(self):
        data = {'title': 'X', 'body': 'Content'}
        serializer = PostSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)
    
    def test_serialization(self):
        post = Post.objects.create(
            title='Test',
            body='Content',
            author=self.user
        )
        serializer = PostSerializer(post)
        self.assertEqual(serializer.data['title'], 'Test')
```

**Serializer Testing**:
- Test validation
- Test serialization output
- Test deserialization
- Test error handling

### Section 179: API Endpoint Testing

```python
from rest_framework.test import APITestCase
from rest_framework import status

class PostAPITest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_list_posts(self):
        response = self.client.get('/api/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_post(self):
        data = {'title': 'New Post', 'body': 'New Content'}
        response = self.client.post('/api/posts/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
    
    def test_create_post_unauthenticated(self):
        self.client.force_authenticate(user=None)
        data = {'title': 'New Post', 'body': 'Content'}
        response = self.client.post('/api/posts/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
```

**API Testing**:
- Test successful requests
- Test error responses
- Test permissions
- Test status codes

### Section 180: Authentication Testing

```python
class AuthenticationTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpass'
        )
    
    def test_login(self):
        response = self.client.post('/api/auth/login/', {
            'username': 'testuser',
            'password': 'testpass'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
    
    def test_login_invalid_password(self):
        response = self.client.post('/api/auth/login/', {
            'username': 'testuser',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_register(self):
        response = self.client.post('/api/auth/registration/', {
            'username': 'newuser',
            'password': 'newpass123',
            'email': 'new@example.com'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CustomUser.objects.filter(username='newuser').exists())
```

**Auth Testing**:
- Test login
- Test registration
- Test token generation
- Test invalid credentials

### Section 181: Permission Testing

```python
class PermissionTest(APITestCase):
    def setUp(self):
        self.author = CustomUser.objects.create_user(username='author')
        self.other_user = CustomUser.objects.create_user(username='other')
        self.post = Post.objects.create(
            title='Post',
            body='Content',
            author=self.author
        )
    
    def test_author_can_edit_post(self):
        self.client.force_authenticate(user=self.author)
        response = self.client.patch(f'/api/posts/{self.post.id}/', {
            'title': 'Updated'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_other_user_cannot_edit_post(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.patch(f'/api/posts/{self.post.id}/', {
            'title': 'Updated'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
```

### Section 182: Running Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test accounts
python manage.py test posts

# Run specific test class
python manage.py test accounts.tests.CustomUserModelTest

# Run specific test method
python manage.py test accounts.tests.CustomUserModelTest.test_user_creation

# Verbose output
python manage.py test -v 2

# Keep database after tests
python manage.py test --keepdb

# Parallel execution
python manage.py test --parallel
```

### Section 183: Test Coverage

```bash
pip install coverage

# Run tests with coverage
coverage run --source='.' manage.py test

# Generate coverage report
coverage report

# Generate HTML coverage report
coverage html

# View report
open htmlcov/index.html
```

**Coverage Reports**:
- Shows which code is tested
- Identifies untested code
- Helps measure test quality
- Target: 80%+ coverage

### Section 184: Fixtures for Test Data

```python
# fixtures/initial_data.json
[
  {
    "model": "accounts.customuser",
    "pk": 1,
    "fields": {
      "username": "testuser",
      "password": "hashed_password",
      "email": "test@example.com"
    }
  }
]

# In test:
class PostTestCase(TestCase):
    fixtures = ['initial_data']
    
    def test_with_fixture_data(self):
        user = CustomUser.objects.get(username='testuser')
        self.assertIsNotNone(user)
```

### Section 185: Mocking External Services

```python
from unittest.mock import patch, Mock

class ExternalServiceTest(APITestCase):
    @patch('requests.post')
    def test_send_email(self, mock_post):
        mock_post.return_value = Mock(status_code=200)
        
        response = self.client.post('/api/auth/registration/', {
            'username': 'newuser',
            'password': 'pass123',
            'email': 'new@example.com'
        })
        
        self.assertTrue(mock_post.called)
```

### Section 186: Performance Testing

```bash
pip install django-silk

# Add to INSTALLED_APPS
INSTALLED_APPS = [
    ...
    'silk',
]

# In urls.py
urlpatterns = [
    path('silk/', include('silk.urls', namespace='silk')),
]

# Run with profiling
# Access: http://localhost:8000/silk/
```

### Section 187: Deployment Preparation

**Production Checklist**:
- [ ] DEBUG = False
- [ ] SECRET_KEY changed
- [ ] ALLOWED_HOSTS configured
- [ ] DATABASES configured for production
- [ ] Static files configured
- [ ] Media files configured
- [ ] Email backend configured
- [ ] Error handling configured
- [ ] Logging configured
- [ ] Security headers configured
- [ ] HTTPS enforced
- [ ] Database backups planned

### Section 188: Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "django_project.wsgi:application", "--bind", "0.0.0.0:8000"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    command: gunicorn django_project.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - SECRET_KEY=your-secret-key
    depends_on:
      - db
  
  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=blog_db
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Section 189: Production Server Setup

```bash
# Install Gunicorn
pip install gunicorn

# Create Systemd service file
sudo nano /etc/systemd/system/django.service

[Unit]
Description=Django Blog API
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/path/to/app
ExecStart=/path/to/app/venv/bin/gunicorn \
    --workers 4 \
    --bind unix:/path/to/app/gunicorn.sock \
    django_project.wsgi:application

[Install]
WantedBy=multi-user.target

# Enable and start service
sudo systemctl enable django
sudo systemctl start django
```

### Section 190: CI/CD Pipeline Configuration

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.11
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python manage.py test
    
    - name: Run migrations
      run: |
        python manage.py migrate
    
    - name: Collect static
      run: |
        python manage.py collectstatic --noinput
```

### Section 191: Monitoring and Logging in Production

```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/django/error.log',
            'maxBytes': 1024 * 1024 * 15,  # 15MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'ERROR',
    },
}
```

### Section 192: Database Migration in Production

```bash
# Create migration
python manage.py makemigrations

# Review migration
python manage.py sqlmigrate app migration_number

# Apply migration with backup
python manage.py dumpdata > pre_migration_backup.json
python manage.py migrate

# Verify
python manage.py migrate --plan
```

### Section 193: Rollback and Recovery

```bash
# Rollback database
python manage.py migrate app migration_number

# Restore from backup
python manage.py loaddata pre_migration_backup.json

# Check migration status
python manage.py showmigrations
```

### Section 194: Health Checks and Monitoring

```python
# health_check view
from django.http import JsonResponse
from django.db import connection

def health_check(request):
    try:
        # Test database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        return JsonResponse({
            'status': 'healthy',
            'database': 'ok'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'unhealthy',
            'error': str(e)
        }, status=503)
```

### Section 195: Performance Optimization in Production

**Optimization Strategies**:
- Enable query caching
- Use database indexes
- Optimize N+1 queries
- Implement pagination
- Use CDN for static files
- Enable gzip compression
- Use database connection pooling
- Monitor slow queries

### Section 196: Security Hardening

```python
# settings.py for production
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_SECURITY_POLICY = {
    'default-src': ("'self'"),
}
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

### Section 197: Database Backup Strategy

```bash
# Regular database backups
0 2 * * * pg_dump blog_db > /backups/backup-$(date +\%Y\%m\%d).sql

# S3 backup
0 3 * * * aws s3 cp /backups/backup-$(date +\%Y\%m\%d).sql \
  s3://backups/blog/

# Verify backup
pg_restore -d blog_test /backups/backup.sql
```

### Section 198: Scaling Considerations

**Horizontal Scaling**:
- Multiple app servers behind load balancer
- Shared database server
- Static files on CDN
- Session store (Redis/Memcached)
- Cache layer (Redis)

### Section 199: Troubleshooting Production Issues

**Common Issues**:
- Database connection errors: Check connection pooling
- Slow queries: Add indexes, optimize
- High memory usage: Profile code, add limits
- High CPU usage: Scale horizontally
- Static files missing: Run collectstatic
- Migrations stuck: Check migration status

### Section 200: Best Practices Summary

**Production Best Practices**:
1. Use environment variables for configuration
2. Implement comprehensive logging
3. Set up monitoring and alerting
4. Automate backups and recovery
5. Use version control for all code
6. Implement CI/CD pipeline
7. Regular security audits
8. Performance monitoring
9. Documented deployment procedure
10. Incident response plan
11. Regular testing and validation
12. Keep dependencies updated

---

## CONCLUSION

This comprehensive 200-section guide covers the complete Django REST API blog application from foundation to production deployment. Each section provides specific, actionable information for implementing and maintaining the application.

### Key Takeaways

- **Architecture**: Django REST Framework provides clean, scalable API architecture
- **Security**: Multiple layers of security (authentication, permissions, CORS)
- **Testing**: Comprehensive testing strategy ensures code quality
- **Deployment**: Multiple deployment options for different scales
- **Monitoring**: Production monitoring ensures reliability

### Next Steps

1. Review sections relevant to current work
2. Implement recommendations progressively
3. Monitor and optimize based on metrics
4. Continuously improve documentation
5. Keep dependencies updated

---

**Document Version**: 1.0
**Last Updated**: 2026-05-29
**Framework**: Django 6.0.5 + DRF 3.17.1
