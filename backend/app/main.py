"""
FastAPI main application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import divination, calendar

app = FastAPI(
    title="周易卜卦系统 API",
    description="智能排盘与卜卦预测系统",
    version="1.0.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(divination.router, prefix="/api/divination", tags=["Divination"])
app.include_router(calendar.router, prefix="/api/calendar", tags=["Calendar"])


@app.get("/")
async def root():
    return {
        "name": "周易卜卦系统",
        "version": "1.0.0",
        "endpoints": {
            "八字排盘": "/api/divination/bazi",
            "万年历": "/api/calendar/convert",
            "节气": "/api/calendar/jieqi"
        }
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
