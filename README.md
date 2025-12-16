# PDF Pages Service with UI (Fixed)

## What was fixed
- Added app/__init__.py
- Fixed uvicorn import path
- Fixed StaticFiles absolute directory

## Run locally
docker build -t pdf-pages .
docker run -p 8000:8000 pdf-pages

## Railway
Deploy directly from GitHub repo