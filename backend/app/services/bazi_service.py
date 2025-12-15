"""
八字排盘服务
BaZi (Four Pillars of Destiny) Chart Generation Service
"""
from datetime import datetime
from typing import Dict, Any, List, Optional
from lunar_python import Solar, Lunar
from .solar_time import get_true_solar_time


# 天干
TIAN_GAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]

# 地支
DI_ZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

# 五行
WU_XING = {
    "甲": "木", "乙": "木",
    "丙": "火", "丁": "火",
    "戊": "土", "己": "土",
    "庚": "金", "辛": "金",
    "壬": "水", "癸": "水",
    "子": "水", "丑": "土", "寅": "木", "卯": "木",
    "辰": "土", "巳": "火", "午": "火", "未": "土",
    "申": "金", "酉": "金", "戌": "土", "亥": "水"
}

# 天干阴阳
GAN_YIN_YANG = {
    "甲": "阳", "乙": "阴",
    "丙": "阳", "丁": "阴",
    "戊": "阳", "己": "阴",
    "庚": "阳", "辛": "阴",
    "壬": "阳", "癸": "阴"
}

# 地支藏干
ZHI_CANG_GAN = {
    "子": ["癸"],
    "丑": ["己", "癸", "辛"],
    "寅": ["甲", "丙", "戊"],
    "卯": ["乙"],
    "辰": ["戊", "乙", "癸"],
    "巳": ["丙", "庚", "戊"],
    "午": ["丁", "己"],
    "未": ["己", "丁", "乙"],
    "申": ["庚", "壬", "戊"],
    "酉": ["辛"],
    "戌": ["戊", "辛", "丁"],
    "亥": ["壬", "甲"]
}

# 十神关系映射
# 生我者印，我生者食伤，克我者官杀，我克者财，同我者比劫
TEN_GODS_RULES = {
    # (日干五行, 其他干五行, 日干阴阳, 其他干阴阳) -> 十神
    ("木", "水", "same"): "正印",
    ("木", "水", "diff"): "偏印",
    ("木", "火", "same"): "伤官",
    ("木", "火", "diff"): "食神",
    ("木", "金", "same"): "正官",
    ("木", "金", "diff"): "七杀",
    ("木", "土", "same"): "正财",
    ("木", "土", "diff"): "偏财",
    ("木", "木", "same"): "比肩",
    ("木", "木", "diff"): "劫财",
    
    ("火", "木", "same"): "正印",
    ("火", "木", "diff"): "偏印",
    ("火", "土", "same"): "伤官",
    ("火", "土", "diff"): "食神",
    ("火", "水", "same"): "正官",
    ("火", "水", "diff"): "七杀",
    ("火", "金", "same"): "正财",
    ("火", "金", "diff"): "偏财",
    ("火", "火", "same"): "比肩",
    ("火", "火", "diff"): "劫财",
    
    ("土", "火", "same"): "正印",
    ("土", "火", "diff"): "偏印",
    ("土", "金", "same"): "伤官",
    ("土", "金", "diff"): "食神",
    ("土", "木", "same"): "正官",
    ("土", "木", "diff"): "七杀",
    ("土", "水", "same"): "正财",
    ("土", "水", "diff"): "偏财",
    ("土", "土", "same"): "比肩",
    ("土", "土", "diff"): "劫财",
    
    ("金", "土", "same"): "正印",
    ("金", "土", "diff"): "偏印",
    ("金", "水", "same"): "伤官",
    ("金", "水", "diff"): "食神",
    ("金", "火", "same"): "正官",
    ("金", "火", "diff"): "七杀",
    ("金", "木", "same"): "正财",
    ("金", "木", "diff"): "偏财",
    ("金", "金", "same"): "比肩",
    ("金", "金", "diff"): "劫财",
    
    ("水", "金", "same"): "正印",
    ("水", "金", "diff"): "偏印",
    ("水", "木", "same"): "伤官",
    ("水", "木", "diff"): "食神",
    ("水", "土", "same"): "正官",
    ("水", "土", "diff"): "七杀",
    ("水", "火", "same"): "正财",
    ("水", "火", "diff"): "偏财",
    ("水", "水", "same"): "比肩",
    ("水", "水", "diff"): "劫财",
}


def get_ten_god(day_gan: str, other_gan: str) -> str:
    """
    计算十神
    
    Args:
        day_gan: 日干（日主）
        other_gan: 其他天干
        
    Returns:
        十神名称
    """
    if day_gan == other_gan:
        return "比肩"
    
    day_wuxing = WU_XING[day_gan]
    other_wuxing = WU_XING[other_gan]
    day_yinyang = GAN_YIN_YANG[day_gan]
    other_yinyang = GAN_YIN_YANG[other_gan]
    
    yy_relation = "same" if day_yinyang == other_yinyang else "diff"
    
    key = (day_wuxing, other_wuxing, yy_relation)
    return TEN_GODS_RULES.get(key, "")


# ========== 身强身弱判断系统 ==========

# 月令旺相休囚死 - 日干在各月支的状态
# 旺: +30, 相: +20, 休: 0, 囚: -10, 死: -20
MONTH_STRENGTH = {
    # 日干五行: {月支: 得分}
    "木": {"寅": 30, "卯": 30, "辰": 20, "亥": 20, "子": 10, "丑": 0, "巳": -10, "午": -10, "未": -10, "申": -20, "酉": -20, "戌": 0},
    "火": {"巳": 30, "午": 30, "未": 20, "寅": 20, "卯": 10, "辰": 0, "申": -10, "酉": -10, "戌": -10, "亥": -20, "子": -20, "丑": 0},
    "土": {"辰": 30, "戌": 30, "丑": 30, "未": 30, "巳": 20, "午": 20, "寅": -10, "卯": -10, "申": 0, "酉": 0, "亥": -10, "子": -10},
    "金": {"申": 30, "酉": 30, "戌": 20, "辰": 20, "丑": 20, "未": 10, "亥": -10, "子": -10, "寅": -20, "卯": -20, "巳": -10, "午": -20},
    "水": {"亥": 30, "子": 30, "丑": 20, "申": 20, "酉": 10, "辰": 0, "寅": -10, "卯": -10, "巳": -20, "午": -20, "未": -10, "戌": 0}
}

# 五行生克关系
WU_XING_RELATIONS = {
    "木": {"生我": "水", "我生": "火", "克我": "金", "我克": "土", "同我": "木"},
    "火": {"生我": "木", "我生": "土", "克我": "水", "我克": "金", "同我": "火"},
    "土": {"生我": "火", "我生": "金", "克我": "木", "我克": "水", "同我": "土"},
    "金": {"生我": "土", "我生": "水", "克我": "火", "我克": "木", "同我": "金"},
    "水": {"生我": "金", "我生": "木", "克我": "土", "我克": "火", "同我": "水"}
}


def calculate_day_master_strength(
    day_gan: str,
    month_zhi: str,
    pillars: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    计算日主强弱
    
    Args:
        day_gan: 日干
        month_zhi: 月支
        pillars: 四柱数据
        
    Returns:
        身强弱分析结果
    """
    day_element = WU_XING[day_gan]
    score = 0
    details = []
    
    # 1. 月令得分 (最重要)
    month_score = MONTH_STRENGTH.get(day_element, {}).get(month_zhi, 0)
    score += month_score
    if month_score >= 20:
        details.append(f"月令{month_zhi}，日主得令(+{month_score})")
    elif month_score <= -10:
        details.append(f"月令{month_zhi}，日主失令({month_score})")
    else:
        details.append(f"月令{month_zhi}，日主平({month_score})")
    
    # 2. 通根分析 - 日干在地支藏干中有根
    root_count = 0
    for pillar in pillars:
        zhi = pillar["zhi"]
        hidden = ZHI_CANG_GAN.get(zhi, [])
        for stem in hidden:
            if WU_XING[stem] == day_element:
                root_count += 1
                score += 8  # 每个根+8分
    
    if root_count > 0:
        details.append(f"通根{root_count}处(+{root_count * 8})")
    
    # 3. 天干生扶
    help_count = 0
    drain_count = 0
    relations = WU_XING_RELATIONS[day_element]
    
    for pillar in pillars:
        if pillar["position"] == "day":
            continue
        gan_element = pillar["gan_element"]
        
        # 生我或同我 = 帮扶
        if gan_element == relations["生我"] or gan_element == day_element:
            help_count += 1
            score += 10
        # 我生或克我 = 耗泄
        elif gan_element == relations["我生"] or gan_element == relations["克我"]:
            drain_count += 1
            score -= 8
    
    if help_count > 0:
        details.append(f"天干帮扶{help_count}(+{help_count * 10})")
    if drain_count > 0:
        details.append(f"天干耗泄{drain_count}(-{drain_count * 8})")
    
    # 4. 确定强弱等级
    if score >= 40:
        level = "极强"
        level_desc = "日主极旺，宜泄不宜扶"
    elif score >= 20:
        level = "偏强"
        level_desc = "日主偏旺，喜耗泄"
    elif score >= -10:
        level = "中和"
        level_desc = "日主中和，综合取用"
    elif score >= -30:
        level = "偏弱"
        level_desc = "日主偏弱，喜生扶"
    else:
        level = "极弱"
        level_desc = "日主极弱，宜扶不宜泄"
    
    return {
        "score": score,
        "level": level,
        "level_desc": level_desc,
        "details": details,
        "day_element": day_element
    }


def calculate_useful_gods(
    day_gan: str,
    strength_result: Dict[str, Any]
) -> Dict[str, Any]:
    """
    计算喜用神
    
    Args:
        day_gan: 日干
        strength_result: 身强弱分析结果
        
    Returns:
        喜用忌神结果
    """
    day_element = WU_XING[day_gan]
    level = strength_result["level"]
    relations = WU_XING_RELATIONS[day_element]
    
    result = {
        "xi_shen": [],      # 喜神
        "yong_shen": None,  # 用神
        "ji_shen": [],      # 忌神
        "xian_shen": []     # 闲神
    }
    
    if level in ["极强", "偏强"]:
        # 身强：喜克泄耗（官杀、食伤、财星）
        result["yong_shen"] = relations["克我"]  # 用官杀
        result["xi_shen"] = [relations["我生"], relations["我克"]]  # 喜食伤、财星
        result["ji_shen"] = [relations["生我"], day_element]  # 忌印星、比劫
        
    elif level in ["极弱", "偏弱"]:
        # 身弱：喜生扶（印星、比劫）
        result["yong_shen"] = relations["生我"]  # 用印星
        result["xi_shen"] = [day_element]  # 喜比劫
        result["ji_shen"] = [relations["克我"], relations["我生"]]  # 忌官杀、食伤
        
    else:  # 中和
        # 中和取平衡
        result["yong_shen"] = relations["我生"]  # 用食伤泄秀
        result["xi_shen"] = [relations["我克"]]  # 喜财星
        result["ji_shen"] = []
    
    # 添加五行名称映射
    element_names = {
        "木": "木（印星）" if relations["生我"] == "木" else ("木（比劫）" if day_element == "木" else "木"),
        "火": "火（印星）" if relations["生我"] == "火" else ("火（比劫）" if day_element == "火" else "火"),
        "土": "土（印星）" if relations["生我"] == "土" else ("土（比劫）" if day_element == "土" else "土"),
        "金": "金（印星）" if relations["生我"] == "金" else ("金（比劫）" if day_element == "金" else "金"),
        "水": "水（印星）" if relations["生我"] == "水" else ("水（比劫）" if day_element == "水" else "水")
    }
    
    return result


def determine_pattern(
    day_gan: str,
    month_zhi: str,
    pillars: List[Dict[str, Any]],
    strength_result: Dict[str, Any]
) -> Dict[str, Any]:
    """
    判断命局格局
    
    Args:
        day_gan: 日干
        month_zhi: 月支
        pillars: 四柱数据
        strength_result: 身强弱结果
        
    Returns:
        格局判断结果
    """
    # 月支藏干取格
    month_hidden = ZHI_CANG_GAN.get(month_zhi, [])
    
    patterns = []
    
    for stem in month_hidden:
        ten_god = get_ten_god(day_gan, stem)
        if ten_god in ["正官", "七杀", "正印", "偏印", "正财", "偏财", "食神", "伤官"]:
            # 检查是否透干
            is_revealed = any(p["gan"] == stem for p in pillars)
            pattern_name = f"{ten_god}格"
            if is_revealed:
                patterns.append({
                    "name": pattern_name,
                    "type": "正格",
                    "revealed": True,
                    "desc": f"月支藏{stem}({ten_god})透干成格"
                })
            else:
                patterns.append({
                    "name": pattern_name,
                    "type": "正格",
                    "revealed": False,
                    "desc": f"月支藏{stem}({ten_god})暗藏"
                })
    
    # 取最显著的格局
    main_pattern = None
    if patterns:
        # 透干的优先
        revealed_patterns = [p for p in patterns if p["revealed"]]
        main_pattern = revealed_patterns[0] if revealed_patterns else patterns[0]
    
    return {
        "main_pattern": main_pattern,
        "all_patterns": patterns,
        "strength_level": strength_result["level"]
    }


def get_da_yun(
    lunar: Lunar,
    gender: int,
    year_gan: str
) -> List[Dict[str, Any]]:
    """
    计算大运
    
    Args:
        lunar: 农历对象
        gender: 1男 0女
        year_gan: 年干
        
    Returns:
        大运列表
    """
    eight_char = lunar.getEightChar()
    yun = eight_char.getYun(gender)
    
    da_yun_list = []
    for dy in yun.getDaYun():
        if dy.getIndex() == 0:
            # 跳过起运前的童限
            continue
        da_yun_list.append({
            "index": dy.getIndex(),
            "start_age": dy.getStartAge(),
            "end_age": dy.getEndAge(),
            "start_year": dy.getStartYear(),
            "end_year": dy.getEndYear(),
            "gan_zhi": dy.getGanZhi()
        })
        if len(da_yun_list) >= 8:
            break
    
    return da_yun_list


def generate_bazi_chart(
    year: int,
    month: int,
    day: int,
    hour: int,
    minute: int = 0,
    longitude: float = 116.4,
    latitude: float = 39.9,
    gender: int = 1,
    use_true_solar_time: bool = True
) -> Dict[str, Any]:
    """
    生成八字命盘
    
    Args:
        year, month, day, hour, minute: 出生时间（公历）
        longitude: 出生地经度
        latitude: 出生地纬度
        gender: 1男 0女
        use_true_solar_time: 是否使用真太阳时
        
    Returns:
        完整的八字命盘数据
    """
    # 原始时间
    original_dt = datetime(year, month, day, hour, minute)
    
    # 真太阳时校正
    solar_correction = None
    if use_true_solar_time:
        true_dt, solar_correction = get_true_solar_time(original_dt, longitude)
        year, month, day = true_dt.year, true_dt.month, true_dt.day
        hour, minute = true_dt.hour, true_dt.minute
    
    # 使用lunar-python计算八字
    solar = Solar.fromYmdHms(year, month, day, hour, minute, 0)
    lunar = solar.getLunar()
    eight_char = lunar.getEightChar()
    
    # 设置流派（1：按子时换日）
    eight_char.setSect(1)
    
    # 四柱
    year_gan = eight_char.getYearGan()
    year_zhi = eight_char.getYearZhi()
    month_gan = eight_char.getMonthGan()
    month_zhi = eight_char.getMonthZhi()
    day_gan = eight_char.getDayGan()
    day_zhi = eight_char.getDayZhi()
    hour_gan = eight_char.getTimeGan()
    hour_zhi = eight_char.getTimeZhi()
    
    # 构建四柱数据
    pillars = [
        {
            "position": "year",
            "position_cn": "年柱",
            "gan": year_gan,
            "zhi": year_zhi,
            "gan_zhi": f"{year_gan}{year_zhi}",
            "gan_element": WU_XING[year_gan],
            "zhi_element": WU_XING[year_zhi],
            "gan_yinyang": GAN_YIN_YANG[year_gan],
            "ten_god": get_ten_god(day_gan, year_gan),
            "hidden_stems": ZHI_CANG_GAN[year_zhi],
            "nayin": eight_char.getYearNaYin()
        },
        {
            "position": "month",
            "position_cn": "月柱",
            "gan": month_gan,
            "zhi": month_zhi,
            "gan_zhi": f"{month_gan}{month_zhi}",
            "gan_element": WU_XING[month_gan],
            "zhi_element": WU_XING[month_zhi],
            "gan_yinyang": GAN_YIN_YANG[month_gan],
            "ten_god": get_ten_god(day_gan, month_gan),
            "hidden_stems": ZHI_CANG_GAN[month_zhi],
            "nayin": eight_char.getMonthNaYin()
        },
        {
            "position": "day",
            "position_cn": "日柱",
            "gan": day_gan,
            "zhi": day_zhi,
            "gan_zhi": f"{day_gan}{day_zhi}",
            "gan_element": WU_XING[day_gan],
            "zhi_element": WU_XING[day_zhi],
            "gan_yinyang": GAN_YIN_YANG[day_gan],
            "ten_god": "日主",
            "hidden_stems": ZHI_CANG_GAN[day_zhi],
            "nayin": eight_char.getDayNaYin()
        },
        {
            "position": "hour",
            "position_cn": "时柱",
            "gan": hour_gan,
            "zhi": hour_zhi,
            "gan_zhi": f"{hour_gan}{hour_zhi}",
            "gan_element": WU_XING[hour_gan],
            "zhi_element": WU_XING[hour_zhi],
            "gan_yinyang": GAN_YIN_YANG[hour_gan],
            "ten_god": get_ten_god(day_gan, hour_gan),
            "hidden_stems": ZHI_CANG_GAN[hour_zhi],
            "nayin": eight_char.getTimeNaYin()
        }
    ]
    
    # 大运
    da_yun = get_da_yun(lunar, gender, year_gan)
    
    # 五行统计
    elements_count = {"木": 0, "火": 0, "土": 0, "金": 0, "水": 0}
    for pillar in pillars:
        elements_count[pillar["gan_element"]] += 1
        elements_count[pillar["zhi_element"]] += 1
    
    # === 新增分析功能 ===
    # 身强身弱
    strength_analysis = calculate_day_master_strength(day_gan, month_zhi, pillars)
    
    # 喜用神
    useful_gods = calculate_useful_gods(day_gan, strength_analysis)
    
    # 格局
    pattern_analysis = determine_pattern(day_gan, month_zhi, pillars, strength_analysis)
    
    return {
        "birth_info": {
            "solar_date": original_dt.strftime("%Y-%m-%d %H:%M"),
            "true_solar_time": f"{year}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}" if use_true_solar_time else None,
            "lunar_date": f"{lunar.getYearInChinese()}年{lunar.getMonthInChinese()}月{lunar.getDayInChinese()}",
            "longitude": longitude,
            "latitude": latitude,
            "gender": "男" if gender == 1 else "女",
            "solar_correction": solar_correction
        },
        "chart": {
            "pillars": pillars,
            "day_master": {
                "gan": day_gan,
                "element": WU_XING[day_gan],
                "yinyang": GAN_YIN_YANG[day_gan]
            },
            "elements_count": elements_count
        },
        "strength_analysis": strength_analysis,
        "useful_gods": useful_gods,
        "pattern_analysis": pattern_analysis,
        "luck_cycles": da_yun,
        "additional_info": {
            "zodiac": lunar.getYearShengXiao(),
            "constellation": solar.getXingZuo(),
            "current_jieqi": lunar.getPrevJieQi().getName() if lunar.getPrevJieQi() else None,
            "next_jieqi": lunar.getNextJieQi().getName() if lunar.getNextJieQi() else None
        }
    }

