import sys
import os
os.environ.setdefault("PYTHONIOENCODING", "utf-8")
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.market import router as market_router
from routers.smc import router as smc_router
from routers.dashboard import router as dashboard_router
from routers.backtest import router as backtest_router

app = FastAPI(title="SMC Backtest API", version="2.0.0")

# Security Hardening: Explicit Origins for Development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
        "http://127.0.0.1:4200",
        "http://localhost:3000",
        "http://127.0.0.1:8000",
        "*"
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Register routers
app.include_router(market_router)
app.include_router(smc_router)
app.include_router(dashboard_router)
app.include_router(backtest_router)

@app.get("/")
def root():
    return {
        "message": "SMC Backtest API is running",
        "version": "2.0.0",
        "docs": "/docs",
        "features": ["market", "smc", "dashboard", "backtest"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
