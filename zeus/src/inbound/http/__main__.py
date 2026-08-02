import uvicorn

from infrastructure.settings import Settings


if __name__ == "__main__":
    settings = Settings()
    uvicorn.run(
        "inbound.http.app:create_app",
        host="0.0.0.0",
        port=settings.zeus.PORT,
        factory=True,
        log_level=settings.zeus.LOG_LEVEL,
        workers=4,
        reload=settings.zeus.DEBUG,
        reload_dirs=settings.zeus.ROOT_DIR,
    )
