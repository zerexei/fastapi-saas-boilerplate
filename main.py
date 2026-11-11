from fastapi import FastAPI

from config import settings


def create_app() -> FastAPI:
    app = FastAPI(
        title="FastAPI SaaS Boilerplate",
        version="0.1.0",
    )

    print(settings)
    @app.get("/healthz", tags=["System"])
    async def health_check():
        return {"status": "healthy"}

    return app


app = create_app()
