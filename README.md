# Darukaa.Earth

## Overview
Darukaa.Earth is a geospatial data analytics platform designed to manage and visualize carbon and biodiversity projects.

## Tech Stack
- **Frontend**: React, Vite, Tailwind CSS
- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL with PostGIS (To be implemented)

## Project Structure
- `frontend/`: React application using Vite.
- `backend/`: FastAPI application.
- `.github/workflows/`: GitHub Actions workflows for CI/CD (To be implemented).

## Local Development

### Frontend
1. `cd frontend`
2. `npm install`
3. `npm run dev`

### Backend
1. `cd backend`
2. `python -m venv .venv`
3. `source .venv/bin/activate` (or `.\.venv\Scripts\activate` on Windows)
4. `pip install -r requirements.txt`
5. `fastapi run app/main.py` (or `uvicorn app.main:app --reload`)

## Environment Variables
Copy `.env.example` to `.env` and fill in the necessary values. See `.env.example` for the required structure.

## Current Development Status
This is the initial scaffolding stage. The frontend and backend applications are running, but no actual features are implemented yet.
PostgreSQL, PostGIS, Mapbox, authentication, and other features will be added in subsequent steps.
