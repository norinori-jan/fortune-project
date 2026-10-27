from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel, Field

from fortune_core.services.runtime_user_platform import (
    FortuneRuntimeUserPlatformService,
)


router = APIRouter(
    prefix="/fortune/user-platform",
    tags=["fortune-user-platform"],
)

_service = FortuneRuntimeUserPlatformService()


class PreferencesRequest(BaseModel):
    theme: str | None = None
    language: str | None = None
    notifications_enabled: bool | None = None
    daily_enabled: bool | None = None
    favorite_systems: list[str] = Field(default_factory=list)


class NotificationRequest(BaseModel):
    enabled: bool | None = None
    morning: bool | None = None
    afternoon: bool | None = None
    evening: bool | None = None


@router.get("/{user_key}")
def get_user_platform(
    user_key: str,
) -> dict:
    return _service.get_user(user_key)


@router.get("/features/list")
def list_features() -> list[dict]:
    return _service.features_snapshot()


@router.get("/{user_key}/preferences")
def get_preferences(
    user_key: str,
) -> dict:
    return _service.preferences.get(
        user_key
    ).to_dict()


@router.put("/{user_key}/preferences")
def update_preferences(
    user_key: str,
    payload: PreferencesRequest,
) -> dict:
    return _service.preferences.update(
        user_key,
        theme=payload.theme,
        language=payload.language,
        notifications_enabled=(
            payload.notifications_enabled
        ),
        daily_enabled=payload.daily_enabled,
        favorite_systems=payload.favorite_systems,
    ).to_dict()


@router.get("/{user_key}/notifications")
def get_notifications(
    user_key: str,
) -> dict:
    return _service.notifications.get(
        user_key
    ).to_dict()


@router.put("/{user_key}/notifications")
def update_notifications(
    user_key: str,
    payload: NotificationRequest,
) -> dict:
    return _service.notifications.update(
        user_key,
        enabled=payload.enabled,
        morning=payload.morning,
        afternoon=payload.afternoon,
        evening=payload.evening,
    ).to_dict()


@router.get("/{user_key}/usage")
def get_usage(
    user_key: str,
) -> dict:
    return _service.usage.get(
        user_key
    ).to_dict()