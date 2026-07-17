from datetime import datetime

from fastapi import APIRouter, HTTPException

from app.schemas import ShichuRequest

from fortune_core.shichu.engine import Engine
from fortune_core.report.paper import PaperBuilder


router = APIRouter()

engine = Engine()
paper_builder = PaperBuilder()


@router.post("/report")
def create_report(req: ShichuRequest):

    try:

        birth = datetime(
            req.year,
            req.month,
            req.day,
            req.hour,
            req.minute,
        )

        chart = engine.generate(
            birth=birth,
            gender=req.gender,
            longitude=req.longitude,
        )

        report = paper_builder.build(chart)

        return report

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )
