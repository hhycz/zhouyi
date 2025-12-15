"""
万年历引擎
Calendar Engine for Lunar/Solar conversion and JieQi calculation
"""
from datetime import datetime
from typing import Optional, Dict, Any
from lunar_python import Lunar, Solar


def solar_to_lunar(year: int, month: int, day: int) -> Dict[str, Any]:
    """
    公历转农历
    
    Args:
        year, month, day: 公历日期
        
    Returns:
        农历信息字典
    """
    solar = Solar.fromYmd(year, month, day)
    lunar = solar.getLunar()
    
    return {
        "solar_date": f"{year}-{month:02d}-{day:02d}",
        "lunar_year": lunar.getYear(),
        "lunar_month": lunar.getMonth(),
        "lunar_day": lunar.getDay(),
        "lunar_month_cn": lunar.getMonthInChinese(),
        "lunar_day_cn": lunar.getDayInChinese(),
        "lunar_date_cn": f"{lunar.getYearInChinese()}年{lunar.getMonthInChinese()}月{lunar.getDayInChinese()}",
        "is_leap_month": lunar.getMonth() < 0,
        "year_gan_zhi": lunar.getYearInGanZhi(),
        "month_gan_zhi": lunar.getMonthInGanZhi(),
        "day_gan_zhi": lunar.getDayInGanZhi(),
        "zodiac": lunar.getYearShengXiao(),
        "jie_qi": lunar.getJieQi() or None,
        "festivals": lunar.getFestivals()
    }


def lunar_to_solar(year: int, month: int, day: int, is_leap: bool = False) -> Dict[str, Any]:
    """
    农历转公历
    
    Args:
        year, month, day: 农历日期
        is_leap: 是否闰月
        
    Returns:
        公历信息字典
    """
    lunar = Lunar.fromYmd(year, -month if is_leap else month, day)
    solar = lunar.getSolar()
    
    return {
        "solar_year": solar.getYear(),
        "solar_month": solar.getMonth(),
        "solar_day": solar.getDay(),
        "solar_date": f"{solar.getYear()}-{solar.getMonth():02d}-{solar.getDay():02d}",
        "weekday": solar.getWeek(),
        "weekday_cn": solar.getWeekInChinese()
    }


def get_jie_qi_list(year: int) -> list:
    """
    获取某年所有节气
    
    Args:
        year: 公历年份
        
    Returns:
        节气列表，包含名称和精确时间
    """
    from lunar_python import LunarYear
    
    lunar_year = LunarYear.fromYear(year)
    jie_qi_list = []
    
    # 获取该年的所有节气
    jq_map = lunar_year.getJieQiJulianDays()
    
    for name, jd in jq_map.items():
        solar = Solar.fromJulianDay(jd)
        jie_qi_list.append({
            "name": name,
            "solar_date": f"{solar.getYear()}-{solar.getMonth():02d}-{solar.getDay():02d}",
            "time": f"{solar.getHour():02d}:{solar.getMinute():02d}:{solar.getSecond():02d}"
        })
    
    return jie_qi_list


def get_today_info() -> Dict[str, Any]:
    """
    获取今日综合信息
    """
    now = datetime.now()
    solar = Solar.fromYmdHms(now.year, now.month, now.day, now.hour, now.minute, now.second)
    lunar = solar.getLunar()
    
    return {
        "solar": {
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M:%S"),
            "weekday": solar.getWeekInChinese()
        },
        "lunar": {
            "year_cn": lunar.getYearInChinese(),
            "month_cn": lunar.getMonthInChinese(),
            "day_cn": lunar.getDayInChinese(),
            "full_date": f"{lunar.getYearInChinese()}年{lunar.getMonthInChinese()}月{lunar.getDayInChinese()}"
        },
        "gan_zhi": {
            "year": lunar.getYearInGanZhi(),
            "month": lunar.getMonthInGanZhi(),
            "day": lunar.getDayInGanZhi(),
            "hour": lunar.getTimeInGanZhi()
        },
        "zodiac": lunar.getYearShengXiao(),
        "jie_qi": lunar.getJieQi(),
        "yi": lunar.getDayYi(),  # 宜
        "ji": lunar.getDayJi(),  # 忌
        "peng_zu": {
            "gan": lunar.getDayPengZuGan(),
            "zhi": lunar.getDayPengZuZhi()
        }
    }
