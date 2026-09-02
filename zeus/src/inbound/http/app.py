from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

from domain.exceptions.base import DomainError
from inbound.http.routes import router as text_router
from infrastructure.containers.application import ApplicationContainer
from infrastructure.containers.utils import create_container
from infrastructure.settings import ZeusSettings


def create_app(*, container: ApplicationContainer | None = None) -> FastAPI:
    description = """
    The `zeus` service is responsible for the text that the user inputs inside the `speedtype` application,
    as well as configuring the typing session.

    The `zeus` service contains words, special symbols, and configuration options that are used to achieve this
    goal.
    """

    container = container or create_container()
    settings: ZeusSettings = container.config.zeus

    app = FastAPI(
        title=settings.APP_NAME,
        description="\n".join(line.strip() for line in description.split("\n")),
        version=settings.VERSION,
        container=container,
    )
    app.include_router(text_router)

    @app.exception_handler(Exception)
    def general_exception_handler(*_args, **_kwargs) -> Response:
        return JSONResponse(
            content={"detail": "Something went wrong..."},
            status_code=500,
        )

    @app.exception_handler(DomainError)
    def domain_error_handler(_request: Request, exc: DomainError) -> Response:
        return JSONResponse(
            content={"detail": str(exc)},
            status_code=400,
        )

    return app
