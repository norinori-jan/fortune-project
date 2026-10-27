from fortune_core.models.api_meta import FortuneApiMeta
def default_api_meta() -> FortuneApiMeta:
    return FortuneApiMeta()
__all__ = [
    "FortuneApiMeta",
    "default_api_meta",
]