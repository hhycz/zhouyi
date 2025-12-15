"""
真太阳时计算服务
True Solar Time calculation based on longitude and Equation of Time
"""
import math
from datetime import datetime, timedelta
from typing import Tuple


def calculate_eot(day_of_year: int) -> float:
    """
    计算真平太阳时差 (Equation of Time)
    
    Args:
        day_of_year: 一年中的第几天 (1-365/366)
        
    Returns:
        时差（分钟），正值表示真太阳时比平太阳时快
    """
    # B = 360/365 * (day - 81), in radians
    B = math.radians(360 / 365 * (day_of_year - 81))
    
    # Equation of Time in minutes
    # EOT = 9.87 * sin(2B) - 7.53 * cos(B) - 1.5 * sin(B)
    eot = 9.87 * math.sin(2 * B) - 7.53 * math.cos(B) - 1.5 * math.sin(B)
    
    return eot


def calculate_longitude_correction(longitude: float, standard_meridian: float = 120.0) -> float:
    """
    计算经度时差
    
    Args:
        longitude: 当地经度
        standard_meridian: 标准时区经度，中国为120°E
        
    Returns:
        时差（分钟），正值表示当地时间比标准时间早
    """
    # 每度经度差4分钟
    return (longitude - standard_meridian) * 4


def get_true_solar_time(
    dt: datetime,
    longitude: float,
    standard_meridian: float = 120.0
) -> Tuple[datetime, dict]:
    """
    计算真太阳时
    
    Args:
        dt: 标准时间（如北京时间）
        longitude: 当地经度
        standard_meridian: 标准时区经度
        
    Returns:
        (真太阳时datetime, 调整详情dict)
    """
    day_of_year = dt.timetuple().tm_yday
    
    # 经度时差
    longitude_correction = calculate_longitude_correction(longitude, standard_meridian)
    
    # 真平太阳时差
    eot = calculate_eot(day_of_year)
    
    # 总时差（分钟）
    total_correction = longitude_correction + eot
    
    # 计算真太阳时
    true_solar_time = dt + timedelta(minutes=total_correction)
    
    correction_details = {
        "original_time": dt.strftime("%Y-%m-%d %H:%M:%S"),
        "true_solar_time": true_solar_time.strftime("%Y-%m-%d %H:%M:%S"),
        "longitude": longitude,
        "longitude_correction_minutes": round(longitude_correction, 2),
        "eot_correction_minutes": round(eot, 2),
        "total_correction_minutes": round(total_correction, 2)
    }
    
    return true_solar_time, correction_details


def get_shichen_from_hour(hour: int) -> Tuple[str, str]:
    """
    根据小时获取时辰
    
    Args:
        hour: 小时 (0-23)
        
    Returns:
        (地支, 时辰名称)
    """
    shichen_map = [
        (23, 1, "子", "子时"),   # 23:00 - 00:59
        (1, 3, "丑", "丑时"),    # 01:00 - 02:59
        (3, 5, "寅", "寅时"),
        (5, 7, "卯", "卯时"),
        (7, 9, "辰", "辰时"),
        (9, 11, "巳", "巳时"),
        (11, 13, "午", "午时"),
        (13, 15, "未", "未时"),
        (15, 17, "申", "申时"),
        (17, 19, "酉", "酉时"),
        (19, 21, "戌", "戌时"),
        (21, 23, "亥", "亥时"),
    ]
    
    for start, end, zhi, name in shichen_map:
        if start <= hour < end or (start == 23 and (hour >= 23 or hour < 1)):
            return zhi, name
    
    return "子", "子时"  # Default
