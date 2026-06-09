from fastapi import FastAPI

from app.config import settings
from app.presentation.api.v1 import books, libraries

app = FastAPI(
    title=settings.app_name,
    description="A simple book management API built with Clean Architecture.",
    version="1.0.0",
)

app.include_router(books.router, prefix="/api/v1")
app.include_router(libraries.router, prefix="/api/v1")


@app.get("/", tags=["health"])
def root() -> dict:
    return {"status": "ok", "service": settings.app_name}
