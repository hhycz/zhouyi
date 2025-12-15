"""
Calendar API routes
"""
from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.models.schemas import CalendarConvertRequest, TrueSolarTimeRequest
from app.services.calendar_engine import (
    solar_to_lunar,
    lunar_to_solar,
    get_jie_qi_list,
    get_today_info
)
from app.services.solar_time import get_true_solar_time

router = APIRouter()


@router.post("/convert", summary="日期转换")
async def convert_date(request: CalendarConvertRequest):
    """
    公历农历互转
    
    - source_type: "solar" 公历转农历，"lunar" 农历转公历
    """
    try:
        if request.source_type == "solar":
            result = solar_to_lunar(request.year, request.month, request.day)
        else:
            result = lunar_to_solar(
                request.year, 
                request.month, 
                request.day,
                request.is_leap_month
            )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"日期转换错误: {str(e)}")


@router.get("/jieqi/{year}", summary="获取节气")
async def get_jieqi(year: int):
    """获取某年所有二十四节气的精确时间"""
    if year < 1900 or year > 2100:
        raise HTTPException(status_code=400, detail="年份超出范围(1900-2100)")
    
    try:
        jieqi_list = get_jie_qi_list(year)
        return {"year": year, "jieqi": jieqi_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"节气计算错误: {str(e)}")


@router.get("/today", summary="今日信息")
async def today_info():
    """获取今日的农历、干支、宜忌等综合信息"""
    try:
        return get_today_info()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取今日信息错误: {str(e)}")


@router.post("/true-solar-time", summary="真太阳时计算")
async def calculate_true_solar_time(request: TrueSolarTimeRequest):
    """
    根据经度计算真太阳时
    
    - 经度时差 = (当地经度 - 120) × 4分钟
    - 还会加上当日真平太阳时差(EOT)
    """
    try:
        dt = datetime(
            request.year,
            request.month,
            request.day,
            request.hour,
            request.minute
        )
        true_time, correction = get_true_solar_time(dt, request.longitude)
        return correction
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"真太阳时计算错误: {str(e)}")
