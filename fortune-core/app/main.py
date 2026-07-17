# app/main.py

from fastapi import FastAPI

from app.routers.shichu import router as shichu_router
from app.routers.iching import router as iching_router
from app.routers.tarot import router as tarot_router


app = FastAPI(
    title="Fortune Project API",
    description="四柱推命・易経・タロット統合API",
    version="1.0.0",
)


# ------------------------------------------------------------
# Routers
# ------------------------------------------------------------

app.include_router(
    shichu_router,
    prefix="/shichu",
    tags=["四柱推命"],
)

app.include_router(
    iching_router,
    prefix="/iching",
    tags=["易経"],
)

app.include_router(
    tarot_router,
    prefix="/tarot",
    tags=["タロット"],
)


# ------------------------------------------------------------
# Root
# ------------------------------------------------------------

@app.get("/")
def root():

    return {
        "application": "Fortune Project API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "shichu": "/shichu/report",
            "iching": "/iching",
            "tarot": "/tarot",
        },
    }


# ------------------------------------------------------------
# Health Check
# ------------------------------------------------------------

@app.get("/health")
def health():

    return {
        "status": "ok",
    }