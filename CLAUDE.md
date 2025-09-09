# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Development Setup
```bash
# Start all services with Docker Compose
docker-compose up -d

# Start backend only (development mode with hot reload)
cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Start frontend only (Vite development server)  
cd frontend && npm run dev

# Install Python dependencies (use virtual environment)
pip install -r requirements.txt

# Install frontend dependencies
cd frontend && npm install
```

### Database Management
```bash
# Apply database migrations
cd backend && alembic upgrade head

# Create new migration (after model changes)
cd backend && alembic revision --autogenerate -m "migration description"

# Database connection: postgresql://postgres:postgres@localhost:5433/claude_fastapi (external port)
```

### Testing and Linting
```bash
# Backend testing (pytest configured but no tests implemented yet)
cd backend && pytest

# Frontend linting
cd frontend && npm run lint

# Frontend build
cd frontend && npm run build
```

## Architecture Overview

**Full-stack FastAPI + Vue.js application** with microservices architecture using Docker containers.

### Core Stack
- **Backend**: FastAPI with SQLAlchemy ORM, PostgreSQL database, Redis caching
- **Frontend**: Vue.js 3 + Vuetify 3 + Vue Router 4 + Vuex 4
- **Infrastructure**: Docker Compose with Nginx reverse proxy
- **Authentication**: JWT-based with access/refresh tokens and bcrypt password hashing

### Key Features
- **Enterprise-ready user management system** with employees, departments, roles, and audit logging
- **Role-based access control (RBAC)** with multiple permission levels
- **Comprehensive API documentation** via FastAPI's built-in Swagger UI at `/docs`
- **Health monitoring** with Redis connectivity checks at `/health`
- **CORS-enabled** for frontend-backend communication

## Project Structure

```
backend/
├── main.py                 # FastAPI application entry point and route registration
├── core/                   # Core configuration and security (JWT, settings)
├── db/base.py             # SQLAlchemy database configuration and session management  
├── models/                 # SQLAlchemy ORM models (User, Employee, Department, Role, SystemLog)
├── schemas/                # Pydantic validation schemas for request/response
├── crud/                   # Database operations layer
├── api/v1/                 # REST API endpoints (auth, users, employees, departments, roles, system-logs)
├── alembic/                # Database migrations with Alembic
└── utils/                  # Utility functions

frontend/
├── src/
│   ├── main.js            # Vue app entry with Vuetify and router setup
│   ├── api/               # Axios HTTP client configuration
│   ├── components/        # Reusable Vue components
│   ├── views/             # Page-level Vue components
│   ├── router/            # Vue Router configuration
│   └── store/             # Vuex state management
└── package.json           # Dependencies and npm scripts
```

## Authentication System

**JWT-based authentication** with the following access patterns:
- `get_current_user()` - Basic authentication check
- `get_current_active_user()` - Requires active user status  
- `get_current_superuser()` - Admin-only access
- `get_current_verified_user()` - Email verification required

**Token Configuration:**
- Access tokens: 30 minutes expiry
- Refresh tokens: 7 days expiry
- Stored in Redis for session management

## Database Architecture

**PostgreSQL with SQLAlchemy ORM** featuring:
- **Users** table with authentication fields
- **Employees** table linked 1:1 with Users
- **Departments** table with hierarchical structure
- **Roles** table with many-to-many User relationships
- **SystemLogs** table for audit trailing

**Migration workflow:**
1. Modify models in `backend/models/`
2. Generate migration: `alembic revision --autogenerate -m "description"`
3. Apply migration: `alembic upgrade head`

## API Endpoints

All API endpoints are prefixed with `/api/v1/` and include:
- `/auth/*` - Authentication (login, register, refresh tokens)
- `/users/*` - User management and profiles
- `/employees/*` - Employee information management
- `/departments/*` - Department and organizational structure
- `/roles/*` - Role-based access control
- `/system-logs/*` - Audit log queries

**API Documentation URLs:**
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`  
- OpenAPI JSON: `http://localhost:8000/openapi.json`

## Environment Configuration

Key environment variables in `.env`:
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string  
- `SECRET_KEY` - JWT signing secret
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiry (default: 30)
- `ALLOWED_ORIGINS` - CORS allowed origins for frontend

## Docker Services

**docker-compose.yml** defines 5 services:
- **backend** (port 8000) - FastAPI application with hot reload
- **frontend** (port 3000) - Vue.js development server
- **nginx** (port 80) - Reverse proxy for production-like routing
- **db** (port 5433 external) - PostgreSQL 15 database
- **redis** (port 6379) - Redis 7 cache with persistence

## Development Notes

- **Hot reload enabled** for both backend and frontend in development
- **Volume mounts** for real-time code changes without rebuilds
- **Health checks** available at `/health` endpoint with Redis connectivity test
- **Cache management** endpoints for Redis testing at `/cache/*`
- **Automatic table creation** on application startup
- **Comprehensive error handling** with proper HTTP status codes

## Testing

- **pytest** configured for backend testing (framework ready, tests not implemented)
- **httpx** included for async HTTP testing
- Run tests with: `cd backend && pytest`