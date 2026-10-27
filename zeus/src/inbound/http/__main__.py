import uvicorn

from infrastructure.containers.utils import create_settings_container


if __name__ == "__main__":
    settings_container = create_settings_container()
    settings = settings_container.config()
    uvicorn.run(
        "inbound.http.app:create_app",
        host="0.0.0.0",
        port=settings.zeus.PORT,
        factory=True,
        log_level=settings.zeus.LOG_LEVEL,
        workers=settings.zeus.WORKERS,
        reload=settings.zeus.DEBUG,
        reload_dirs=str(settings.zeus.ROOT_DIR),
    )
