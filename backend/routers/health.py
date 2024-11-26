from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health_check():
    """
    Health check endpoint to verify whether the server is running.
    """
    return {"status": "ok"}
