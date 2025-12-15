"""
Divination API routes
"""
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel, Field
from app.models.schemas import BaziRequest, BaziResponse
from app.services.bazi_service import generate_bazi_chart
from app.services.liuyao_service import generate_liuyao_chart, simulate_coin_toss

router = APIRouter()


class LiuyaoRequest(BaseModel):
    """六爻起卦请求"""
    question: str = Field("", description="所问之事")
    coin_results: Optional[List[int]] = Field(None, description="六次抛币结果(6-9),为空则自动模拟")
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "事业前景如何",
                "coin_results": [7, 8, 7, 9, 8, 6]
            }
        }


@router.post("/bazi", summary="八字排盘", response_model=BaziResponse)
async def get_bazi_chart(request: BaziRequest):
    """
    根据出生时间和地点生成八字命盘
    
    - **birth_year**: 出生年（公历）
    - **birth_month**: 出生月
    - **birth_day**: 出生日
    - **birth_hour**: 出生小时
    - **birth_minute**: 出生分钟
    - **longitude**: 出生地经度（用于真太阳时计算）
    - **latitude**: 出生地纬度
    - **gender**: 1男 0女（影响大运顺逆）
    - **use_true_solar_time**: 是否启用真太阳时校正
    """
    try:
        result = generate_bazi_chart(
            year=request.birth_year,
            month=request.birth_month,
            day=request.birth_day,
            hour=request.birth_hour,
            minute=request.birth_minute,
            longitude=request.longitude,
            latitude=request.latitude,
            gender=request.gender,
            use_true_solar_time=request.use_true_solar_time
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"排盘计算错误: {str(e)}")


@router.post("/liuyao", summary="六爻起卦")
async def get_liuyao_chart(request: LiuyaoRequest):
    """
    六爻金钱卦起卦
    
    - **question**: 所问之事
    - **coin_results**: 六次抛币结果(6=老阴,7=少阳,8=少阴,9=老阳)
    
    如果不传coin_results，系统会自动模拟抛币
    返回包含卦象和卦辞解读的完整数据
    """
    from app.services.interpretation_service import generate_interpretation
    
    try:
        result = generate_liuyao_chart(
            coin_results=request.coin_results,
            question=request.question
        )
        
        # 获取卦辞解读
        interpretation = generate_interpretation(
            hexagram_name=result.get("original_hexagram", {}).get("name", ""),
            changed_hexagram_name=result.get("changed_hexagram", {}).get("name") if result.get("changed_hexagram") else None,
            moving_positions=result.get("moving_positions", []),
            question=request.question
        )
        
        # 合并结果
        result["interpretation"] = interpretation
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"起卦计算错误: {str(e)}")


@router.get("/liuyao/toss", summary="模拟抛币")
async def toss_coin():
    """模拟一次抛三枚铜钱"""
    result = simulate_coin_toss()
    coin_names = {6: "老阴", 7: "少阳", 8: "少阴", 9: "老阳"}
    return {
        "value": result,
        "name": coin_names.get(result, ""),
        "is_yang": result in [7, 9],
        "is_changing": result in [6, 9]
    }


class AIInterpretRequest(BaseModel):
    """AI解卦请求"""
    question: str = Field("", description="所问之事")
    hexagram_name: str = Field(..., description="本卦名称")
    changed_hexagram_name: Optional[str] = Field(None, description="变卦名称")
    moving_positions: Optional[List[int]] = Field(None, description="动爻位置")
    interpretation_data: Optional[dict] = Field(None, description="基础解读数据")


@router.post("/liuyao/ai-interpret", summary="AI智能解卦")
async def ai_interpret(request: AIInterpretRequest):
    """
    使用 Gemini AI 进行智能解卦
    
    需要设置环境变量 GEMINI_API_KEY
    """
    from app.services.gemini_service import generate_ai_interpretation
    
    try:
        result = await generate_ai_interpretation(
            question=request.question,
            hexagram_name=request.hexagram_name,
            changed_hexagram_name=request.changed_hexagram_name,
            moving_positions=request.moving_positions or [],
            interpretation_data=request.interpretation_data
        )
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return {
            "success": True,
            "content": result["content"]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI解卦错误: {str(e)}")


@router.get("/test", summary="测试接口")
async def test_endpoint():
    """测试八字排盘接口"""
    test_result = generate_bazi_chart(
        year=1995,
        month=10,
        day=27,
        hour=10,
        minute=30,
        longitude=116.4,
        latitude=39.9,
        gender=1
    )
    return test_result

