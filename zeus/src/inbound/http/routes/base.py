from fastapi import APIRouter


router = APIRouter(
    tags=["Common"],
)


@router.get("/health")
def health() -> None:
    """
    Zeus's health check endpoint.
    """
    return
