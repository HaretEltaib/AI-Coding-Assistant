from fastapi import APIRouter, status


router = APIRouter()

@router.get("/health")
def health():
    return {"status": status.HTTP_200_OK , "message": "OK"}

