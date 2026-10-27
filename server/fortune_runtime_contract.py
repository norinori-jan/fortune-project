from __future__ import annotations

from fastapi import APIRouter

from fortune_core.services.runtime_contract import (
    FortuneRuntimeContractService,
)


router = APIRouter(
    prefix="/fortune/contract",
    tags=["fortune-contract"],
)

_service = FortuneRuntimeContractService()


@router.get("")
def runtime_contract() -> dict:
    return _service.get().to_dict()