# Cloud Centric Application
A cloud-native backend appliaction built with FastAPI, PostgreSQL, SQLAlchemy, and Alembic, fully containerized using Docker and orchestrated locally via Docker Compose

This project follows production-grade patterns:
- Database migrations (Alembic)
- Environment-based configuration
- Container networking
- Metrics for observability
- Ready for CI/CD & Kubernetes

## Tech stack
- Backend: FastAPI (Python 3.12)
- Database: PostgreSQL 15
- ORM: SQLAlchemy
- Migrations: Alembic
- Containerization: Docker, Docker Compose
- Metrics: Prometheus client
- Testing: Pytest, HTTPX

## Prerequisites
- docker
- docker compose
- git

## Run the application locally

### Clone the repository
- git clone <repo-url>
- cd CloudCentricApplication

### Build and start services
- docker compose up --build
This starts:
1. FastAPI API (http://localhost:8000) 
2. PostgreSQL database
3. Applies Alembic migrations automatically

### verify the application
1. http://localhost:8000/docs
2. http://localhost:8000/metrics

### Database and migrations

#### Generate a new migration: run incside docker network (recommended):
- docker compose run api alembic revision --autogenerate -m "describe change"
#### Apply migrations
- docker compose run api alembic upgrade head
Tables are versioned and tracked via the alembic_version table.

### Local API Testing: create an item
- create an item
   curl -X POST http://localhost:8000/items \
  -H "Content-Type: application/json" \
  -d '{"name":"docker","description":"running in container"}'
- fetch items
  curl http://localhost:8000/items

### Environment Configuration
The application uses environment variables:
- DATABASE_URL=postgresql://postgres:postgres@db:5432/appdb
db is the Docker Compose service name
Do not use localhost inside containers

## Reference
<!-- ```bash
code block -->
