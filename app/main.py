from app.routers import route_auth
from fastapi import FastAPI

api_title = "Auth"
api_version = "0.0.1"
api_description = "Auth and registration"

app = FastAPI(title=api_title, version=api_version, description=api_description)

app.include_router(route_auth.router, prefix="/api")
