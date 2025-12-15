"""
Pydantic schemas for API request/response
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class BaziRequest(BaseModel):
    """八字排盘请求"""
    birth_year: int = Field(..., ge=1900, le=2100, description="出生年（公历）")
    birth_month: int = Field(..., ge=1, le=12, description="出生月")
    birth_day: int = Field(..., ge=1, le=31, description="出生日")
    birth_hour: int = Field(..., ge=0, le=23, description="出生小时")
    birth_minute: int = Field(0, ge=0, le=59, description="出生分钟")
    longitude: float = Field(116.4, ge=-180, le=180, description="出生地经度")
    latitude: float = Field(39.9, ge=-90, le=90, description="出生地纬度")
    gender: int = Field(1, ge=0, le=1, description="性别：1男 0女")
    use_true_solar_time: bool = Field(True, description="是否使用真太阳时")
    
    class Config:
        json_schema_extra = {
            "example": {
                "birth_year": 1995,
                "birth_month": 10,
                "birth_day": 27,
                "birth_hour": 10,
                "birth_minute": 30,
                "longitude": 116.4,
                "latitude": 39.9,
                "gender": 1
            }
        }


class PillarInfo(BaseModel):
    """单柱信息"""
    position: str
    position_cn: str
    gan: str
    zhi: str
    gan_zhi: str
    gan_element: str
    zhi_element: str
    gan_yinyang: str
    ten_god: str
    hidden_stems: List[str]
    nayin: str


class DayMaster(BaseModel):
    """日主信息"""
    gan: str
    element: str
    yinyang: str


class LuckCycle(BaseModel):
    """大运信息"""
    index: int
    start_age: int
    end_age: int
    start_year: int
    end_year: int
    gan_zhi: str


class BirthInfo(BaseModel):
    """出生信息"""
    solar_date: str
    true_solar_time: Optional[str]
    lunar_date: str
    longitude: float
    latitude: float
    gender: str
    solar_correction: Optional[Dict[str, Any]]


class ChartInfo(BaseModel):
    """命盘信息"""
    pillars: List[PillarInfo]
    day_master: DayMaster
    elements_count: Dict[str, int]


class AdditionalInfo(BaseModel):
    """附加信息"""
    zodiac: str
    constellation: str
    current_jieqi: Optional[str]
    next_jieqi: Optional[str]


class BaziResponse(BaseModel):
    """八字排盘响应"""
    birth_info: BirthInfo
    chart: ChartInfo
    luck_cycles: List[LuckCycle]
    additional_info: AdditionalInfo


class CalendarConvertRequest(BaseModel):
    """日期转换请求"""
    year: int = Field(..., ge=1900, le=2100)
    month: int = Field(..., ge=1, le=12)
    day: int = Field(..., ge=1, le=31)
    source_type: str = Field("solar", description="solar公历 or lunar农历")
    is_leap_month: bool = Field(False, description="农历转公历时是否闰月")


class TrueSolarTimeRequest(BaseModel):
    """真太阳时计算请求"""
    year: int
    month: int
    day: int
    hour: int
    minute: int = 0
    longitude: float = Field(..., description="当地经度")
