# FastAPI Backend – Social Media API

A backend REST API built using **FastAPI, PostgreSQL, SQLAlchemy and Python**. This project implements user authentication, JWT-based authorization, CRUD operations for posts, voting functionality, automated testing, Docker containerization and CI/CD using GitHub Actions.

## Features

- User registration and login
- Secure password hashing using Passlib and bcrypt
- JWT access token authentication
- OAuth2 Bearer token authorization
- Create, read, update and delete posts
- User-specific post authorization
- Search and pagination for posts
- Upvote and remove votes on posts
- PostgreSQL database integration
- Database migrations using Alembic
- Automated testing using Pytest
- Docker containerization
- Docker Compose for multi-container setup
- Automated CI/CD using GitHub Actions
- Automatic Docker image publishing to Docker Hub

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| FastAPI | REST API framework |
| PostgreSQL | Relational database |
| SQLAlchemy | ORM and database operations |
| Pydantic | Data validation |
| Alembic | Database migrations |
| Passlib & bcrypt | Password hashing |
| Python-JOSE | JWT authentication |
| Pytest | Automated testing |
| Docker | Containerization |
| Docker Compose | Multi-container management |
| GitHub Actions | CI/CD automation |
| Gunicorn | Application server |
| NGINX | Reverse proxy |

## Project Structure

```text
fastapi/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── alembic/
│   └── versions/
│
├── app/
│   ├── routers/
│   │   ├── auth.py
│   │   ├── post.py
│   │   ├── user.py
│   │   └── vote.py
│   │
│   ├── config.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── oauth2.py
│   ├── schemas.py
│   └── utils.py
│
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_basic.py
│   ├── test_class.py
│   ├── test_exceptions.py
│   ├── test_fixtures.py
│   ├── test_main.py
│   ├── test_parametrize.py
│   ├── test_posts.py
│   └── test_users.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── alembic.ini
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/pallavikambali/fastapi.git
cd fastapi
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Ubuntu/Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
pip install pytest httpx2
```

### 4. Configure environment variables

Create a `.env` file in the project root.

Add your own PostgreSQL credentials and secret key:

```env
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_USERNAME=your_username
DATABASE_PASSWORD=your_password
DATABASE_NAME=fastapi

SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Important:** Never commit your `.env` file or expose your secret key or database password.

### 5. Run database migrations

```bash
alembic upgrade head
```

Make sure PostgreSQL is running and the database exists before running migrations.

### 6. Start the FastAPI server

```bash
uvicorn app.main:app --reload
```

The application will be available at:

```text
http://127.0.0.1:8000
```

## API Documentation

FastAPI provides interactive API documentation.

- Swagger UI: `/docs`
- ReDoc: `/redoc`

### API Endpoints

#### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/login` | Authenticate user and generate JWT token |

#### Users

| Method | Endpoint | Description |
|---|---|---|
| POST | `/users/` | Register a new user |
| GET | `/users/{id}` | Retrieve user details |

#### Posts

| Method | Endpoint | Description |
|---|---|---|
| GET | `/posts/` | Retrieve posts |
| POST | `/posts/` | Create a post |
| GET | `/posts/{id}` | Retrieve a specific post |
| PUT | `/posts/{id}` | Update a post |
| DELETE | `/posts/{id}` | Delete a post |

The posts endpoint supports search, limit and skip parameters.

#### Votes

| Method | Endpoint | Description |
|---|---|---|
| POST | `/vote/` | Add or remove a vote |

Most post and voting operations require a valid JWT Bearer token.

Users can modify or delete only their own posts.

## Docker Setup

This project supports Docker and Docker Compose.

### Build and start containers

```bash
docker compose up --build
```

This starts:

- FastAPI application container
- PostgreSQL database container

The API is available at:

```text
http://localhost:8000
```

Stop the containers:

```bash
docker compose down
```

### Docker Hub

The Docker image is published automatically to:

**Docker Hub Repository:**  
https://hub.docker.com/r/pallavikambali/fastapi-app

Pull the image:

```bash
docker pull pallavikambali/fastapi-app:latest
```

## Automated Testing

The project uses Pytest to test API functionality.

Run all tests:

```bash
python -m pytest -v
```

The test suite covers:

- Authentication and login
- JWT token validation
- User registration
- Post creation and retrieval
- Post updates and deletion
- Authorization checks
- Error handling
- Fixtures and parametrized tests

**Latest local test result: 34 passed.**

## CI/CD Pipeline

GitHub Actions automates testing and Docker image publishing.

Workflow configuration:

`.github/workflows/ci.yml`

### Pipeline workflow

1. Code is pushed to the `main` branch.
2. GitHub Actions starts the workflow.
3. Python environment is configured.
4. Dependencies are installed.
5. PostgreSQL test database is started.
6. Automated tests are executed.
7. If all tests pass, GitHub Actions logs in to Docker Hub.
8. Docker image is built and pushed automatically.

Docker publishing is restricted to successful pushes to the `main` branch. Pull requests run tests without publishing images.

Docker Hub credentials are securely configured using GitHub repository secrets.

## Deployment

The application has also been practised in an Ubuntu Linux environment using:

- SSH
- Gunicorn
- Systemd
- NGINX

These tools provide application process management and reverse proxy functionality.

## Learning Outcomes

Through this project, I gained practical experience with:

- Building REST APIs using FastAPI
- Database integration using PostgreSQL and SQLAlchemy
- Authentication and authorization using JWT and OAuth2
- Database migrations using Alembic
- Writing automated tests using Pytest
- Containerizing applications using Docker
- Managing multi-container applications using Docker Compose
- Implementing CI/CD pipelines using GitHub Actions
- Deploying backend applications on Ubuntu Linux

## Author

**Pallavi Kambali**

GitHub: [@pallavikambali](https://github.com/pallavikambali)

---

If you found this project interesting, feel free to explore the repository!
