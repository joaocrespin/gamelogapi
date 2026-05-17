# GameLog API

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)

A REST API for gamers to register, review, and track their gaming journey. Built as a portfolio project to consolidate backend development concepts with a real-world use case.

---

## Features

- User registration and login with JWT authentication
- Personal game library with status tracking: `playing`, `completed`, `dropped`, `wishlist`
- Game reviews with star rating and text
- Game search by name, genre, and platform
- `/stats` endpoint with user metrics
- `/trending` endpoint powered by Redis cache
- `/recommendations` endpoint with similarity-based logic

---

## Tech Stack

| Technology | Purpose |
|---|---|
| FastAPI | Web framework |
| PostgreSQL | Relational database |
| SQLAlchemy + Alembic | ORM and migrations |
| PyJWT | Authentication |
| Redis | Cache layer |
| Pytest | Unit testing |
| Docker + Docker Compose | Containerization |

---

## Project Structure

```
gamelog-api/
├── app/
│   ├── api/          # Routers (endpoints)
│   ├── core/         # Database and cache configuration
│   ├── models/       # SQLAlchemy models
│   ├── schemas/      # Pydantic schemas
│   ├── services/     # Business logic
│   └── main.py
├── tests/
│   └── unit/
├── alembic/          # Database migrations
├── docker-compose.yml
├── Dockerfile
└── README.md
```

---

## Running Locally

### Prerequisites

- Python 3.12+
- PostgreSQL running on port 5432
- Redis running on port 6379

### Setup

```bash
# Clone the repository
git clone https://github.com/joaocrespin/gamelogapi.git
cd gamelogapi

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```


### Start the server

```bash
fastapi dev app/main.py
```

The API will be available at `http://localhost:8000` and the interactive docs at `http://localhost:8000/docs`.

---

## Running with Docker

### Prerequisites

- Docker
- Docker Compose

### Setup

```bash
# Clone the repository
git clone https://github.com/joaocrespin/gamelogapi.git
cd gamelogapi
```

Set the environment variables in `docker-compose.yml` under the `app` service, then run:

```bash
docker compose up -d --build
```

The API will be available at `http://localhost:8000`.

---

## Running Tests

```bash
PYTHONPATH=app pytest
```

---

## API Overview

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/user/register` | Register a new user | No |
| POST | `/user/login` | Login and receive JWT token | No |
| GET | `/user/me` | Get current user profile | Yes |
| GET | `/status/` | Get user stats | No |
| POST | `/games/create` | Add a new game | Yes |
| GET | `/games/{id}` | Get game by ID | Yes |
| GET | `/games/` | Search games | No |
| PUT | `/games/{id}` | Update a game | Yes |
| DELETE | `/game/{id}` | Delete a game | Yes |
| POST | `/library/create` | Add game to library | Yes |
| GET | `/library/{id}` | Get library entry | Yes |
| PUT | `/library/{id}` | Update library entry | Yes |
| DELETE | `/library/{id}` | Delete library entry | Yes |
| POST | `/review/create` | Create a review | Yes |
| GET | `/review/{id}` | Get review | Yes |
| PUT | `/review/{id}` | Update review | Yes |
| DELETE | `/review/{id}` | Delete review | Yes |
| GET | `/trending/game` | Get trending game | No |
| GET | `/recommendations` | Get game recommendations | Yes |