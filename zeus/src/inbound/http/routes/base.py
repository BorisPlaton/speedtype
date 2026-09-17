from fastapi import APIRouter, status


router = APIRouter(
    tags=["Common"],
)


@router.get(
    "/health",
    status_code=status.HTTP_204_NO_CONTENT,
)
def health() -> None:
    """
    Zeus's health check endpoint.
    """
    return
