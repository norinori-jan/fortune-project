# app/routers/iching.py

from fastapi import APIRouter, HTTPException

from app.schemas import IChingRequest

from fortune_core.iching.hexagrams import HexagramEngine


router = APIRouter()

engine = HexagramEngine()


@router.post("/reading")
def create_reading(
    req: IChingRequest,
):

    try:

        result = engine.generate(
            numbers=req.numbers,
        )

        return result

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


@router.get("/")
def index():

    return {
        "service": "I Ching",
        "endpoint": "/iching/reading",
    }