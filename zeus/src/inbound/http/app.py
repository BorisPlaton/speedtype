from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from inbound.http.routes import router as text_router
from infrastructure.containers.application import ApplicationContainer
from infrastructure.settings import Settings


def create_app() -> FastAPI:
    description = """
    The `zeus` service is responsible for the text that the user inputs inside the `speedtype` application,
    as well as configuring the typing session.

    The `zeus` service contains words, special symbols, and configuration options that are used to achieve this
    goal.
    """

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
        description="\n".join(line.strip() for line in description.split("\n")),
        version=settings.zeus.VERSION,
    )
    app.include_router(text_router)

    return app
