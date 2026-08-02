from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from inbound.http.routes import router as text_router
from infrastructure.containers.application import ApplicationContainer
from infrastructure.settings import Settings


def create_app() -> FastAPI:
    @asynccontextmanager
    async def lifespan(*_args, **_kwargs) -> AsyncIterator[None]:
        app.state.container = container
        yield

    container = ApplicationContainer()
    settings = Settings()
    container.config.from_pydantic(settings)

    app = FastAPI(
        title=settings.zeus.APP_NAME,
        lifespan=lifespan,
    )
    app.include_router(text_router)

    return app
