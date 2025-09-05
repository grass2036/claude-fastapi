# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a full-stack web application built with FastAPI (backend) and Vue.js 3 (frontend), featuring a PostgreSQL database and Redis cache. The application includes user authentication, a management dashboard, and various administrative features.

## Architecture

### Backend Structure
- **Main Application**: Located in both `app/` (simple version) and `backend/` (full structure)
- **Core Components**:
  - `backend/main.py`: Main FastAPI application with lifespan management
  - `backend/core/config.py`: Settings and configuration management
  - `backend/api/v1/`: Versioned API endpoints (auth implemented)
  - `backend/models/`: SQLAlchemy database models
  - `backend/schemas/`: Pydantic request/response schemas
  - `backend/crud/`: Database CRUD operations
  - `backend/db/`: Database connection and session management
  - `backend/alembic/`: Database migrations

### Frontend Structure
- **Framework**: Vue.js 3 with Composition API, Vuetify UI framework
- **Key Components**:
  - `frontend/src/router/index.js`: Vue Router with authentication guards
  - `frontend/src/store/index.js`: Vuex state management (currently using mock data)
  - `frontend/src/views/`: Page components (Dashboard, Users, Login, Register, etc.)
  - Authentication flow implemented with localStorage persistence

### Infrastructure
- **Docker**: Multi-service setup with backend, frontend, database, Redis, and Nginx
- **Database**: PostgreSQL with Alembic migrations
- **Cache**: Redis for session management and caching
- **Reverse Proxy**: Nginx for production deployment

## Common Commands

### Development (Docker)
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f [service_name]

# Rebuild specific service
docker-compose build [service_name]
docker-compose up -d [service_name]

# Stop all services
docker-compose down
```

### Backend Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run development server (from backend directory)
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Database migrations
alembic upgrade head
alembic revision --autogenerate -m "description"

# Run tests (if available)
pytest
```

### Frontend Development
```bash
# Install dependencies
cd frontend && npm install

# Development server
npm run dev
# or
npm run serve

# Build for production
npm run build

# Lint code
npm run lint
```

### Environment Configuration
- Copy `.env.example` to `.env` and configure values
- Key settings include database URL, Redis URL, JWT secret, and CORS origins
- Frontend API URL configured via `VUE_APP_API_URL` environment variable

## Application State

### Backend Status
- Basic FastAPI structure implemented
- Redis integration working (cache endpoints available)
- Authentication API structure in place (`backend/api/v1/auth.py`)
- Database models and migrations configured but not fully implemented
- Health check and cache test endpoints available

### Frontend Status
- Core UI components fully implemented (Login, Register, Dashboard, Users management)
- Authentication flow working with mock data
- State management via Vuex with localStorage persistence
- Incomplete features: Logs, Settings, Monitoring (placeholders exist)
- Uses demo/mock authentication - not connected to backend API yet

### Integration Points
- Frontend currently uses mock authentication and user data
- Backend authentication endpoints exist but frontend not yet integrated
- CORS configured for local development (localhost:3000)
- API base URL configurable via environment variables

## Key Development Notes

### Authentication Flow
- Backend: JWT-based authentication structure ready
- Frontend: Mock authentication with localStorage persistence
- Integration needed: Connect frontend auth to backend API endpoints

### Database Schema
- Alembic configured for migrations
- Models defined but may need completion
- PostgreSQL as primary database with Redis for caching

### Deployment
- Production ready with Docker Compose
- Nginx reverse proxy configured
- Environment-based configuration
- See `DEPLOYMENT.md` for detailed deployment instructions

## Testing
- Backend: pytest configured but tests may need implementation
- Frontend: No test framework currently configured
- Health check endpoints available for monitoring