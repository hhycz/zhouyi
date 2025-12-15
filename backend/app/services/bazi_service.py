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
# 阴阳规则：同阴阳为偏，异阴阳为正
TEN_GODS_RULES = {
    # (日干五行, 其他干五行, 阴阳关系) -> 十神
    # same = 同阴阳 -> 偏系 (七杀、偏印、偏财、食神、比肩)
    # diff = 异阴阳 -> 正系 (正官、正印、正财、伤官、劫财)
    
    ("木", "水", "diff"): "正印",
    ("木", "水", "same"): "偏印",
    ("木", "火", "diff"): "伤官",
    ("木", "火", "same"): "食神",
    ("木", "金", "diff"): "正官",
    ("木", "金", "same"): "七杀",
    ("木", "土", "diff"): "正财",
    ("木", "土", "same"): "偏财",
    ("木", "木", "same"): "比肩",
    ("木", "木", "diff"): "劫财",
    
    ("火", "木", "diff"): "正印",
    ("火", "木", "same"): "偏印",
    ("火", "土", "diff"): "伤官",
    ("火", "土", "same"): "食神",
    ("火", "水", "diff"): "正官",
    ("火", "水", "same"): "七杀",
    ("火", "金", "diff"): "正财",
    ("火", "金", "same"): "偏财",
    ("火", "火", "same"): "比肩",
    ("火", "火", "diff"): "劫财",
    
    ("土", "火", "diff"): "正印",
    ("土", "火", "same"): "偏印",
    ("土", "金", "diff"): "伤官",
    ("土", "金", "same"): "食神",
    ("土", "木", "diff"): "正官",
    ("土", "木", "same"): "七杀",
    ("土", "水", "diff"): "正财",
    ("土", "水", "same"): "偏财",
    ("土", "土", "same"): "比肩",
    ("土", "土", "diff"): "劫财",
    
    ("金", "土", "diff"): "正印",
    ("金", "土", "same"): "偏印",
    ("金", "水", "diff"): "伤官",
    ("金", "水", "same"): "食神",
    ("金", "火", "diff"): "正官",
    ("金", "火", "same"): "七杀",
    ("金", "木", "diff"): "正财",
    ("金", "木", "same"): "偏财",
    ("金", "金", "same"): "比肩",
    ("金", "金", "diff"): "劫财",
    
    ("水", "金", "diff"): "正印",
    ("水", "金", "same"): "偏印",
    ("水", "木", "diff"): "伤官",
    ("水", "木", "same"): "食神",
    ("水", "土", "diff"): "正官",
    ("水", "土", "same"): "七杀",
    ("水", "火", "diff"): "正财",
    ("水", "火", "same"): "偏财",
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
# 月令旺相休囚死 - 日干在各月支的状态
# 旺: +30 (得令), 相: +20, 休: 0, 囚: -10, 死: -30 (失令)
MONTH_STRENGTH = {
    # 日干五行: {月支: 得分}
    "木": {"寅": 30, "卯": 30, "辰": 10, "亥": 20, "子": 20, "丑": 0, "巳": -10, "午": -10, "未": 0, "申": -30, "酉": -30, "戌": 0},
    "火": {"巳": 30, "午": 30, "未": 10, "寅": 20, "卯": 20, "辰": -10, "申": -20, "酉": -20, "戌": 10, "亥": -30, "子": -30, "丑": -10},
    "土": {"辰": 30, "戌": 30, "丑": 30, "未": 30, "巳": 20, "午": 20, "寅": -20, "卯": -20, "申": -10, "酉": -10, "亥": -20, "子": -20},
    "金": {"申": 30, "酉": 30, "戌": 10, "辰": 10, "丑": 10, "未": 0, "亥": -20, "子": -20, "寅": -30, "卯": -30, "巳": -10, "午": -20},
    "水": {"亥": 30, "子": 30, "丑": 10, "申": 20, "酉": 20, "辰": 0, "寅": -20, "卯": -20, "巳": -30, "午": -30, "未": -10, "戌": -10}
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
    计算日主强弱 (P0核心升级版)
    
    评分标准:
    1. 月令 (30-40%权重): 得令+30, 相+20, 休0, 囚-10, 死-30
    2. 通根:
       - 本气根 (如甲见寅): +15
       - 中气根 (如甲见亥中甲): +10
       - 余气根 (如甲见辰中乙): +5
    3. 天干:
       - 帮扶 (比劫/印): +10
       - 克泄耗 (官杀/食伤/财): -10
    
    总分判定:
    >= 50: 极强
    30 ~ 49: 偏强
    -10 ~ 29: 中和
    -30 ~ -11: 偏弱
    <= -31: 极弱
    """
    day_element = WU_XING[day_gan]
    score = 0
    details = []
    
    # 1. 月令得分
    month_score = MONTH_STRENGTH.get(day_element, {}).get(month_zhi, 0)
    score += month_score
    if month_score >= 20:
        details.append(f"月令{month_zhi}，得令(+{month_score})")
    elif month_score <= -10:
        details.append(f"月令{month_zhi}，失令({month_score})")
    else:
        details.append(f"月令{month_zhi}，平常({month_score})")
    
    # 2. 通根分析 (更精细的根气计算)
    # 简单查表法: 地支藏干
    # 这里我们简化处理: 检查地支藏干中是否有同我五行
    root_score = 0
    roots_found = []
    
    for pillar in pillars:
        zhi = pillar["zhi"]
        hidden = ZHI_CANG_GAN.get(zhi, [])
        
        # 判断根的力度
        # 简化逻辑: 如果藏干第一位(本气)是同我/生我 -> 强根
        main_energy = hidden[0]
        main_element = WU_XING[main_energy]
        
        current_root_score = 0
        is_root = False
        
        # 遍历藏干寻找比劫(同我)
        for stem in hidden:
            if WU_XING[stem] == day_element:
                is_root = True
                # 本气 (通常在第一个)
                if stem == hidden[0]:
                    current_root_score = 15
                else:
                    # 中气/余气
                    current_root_score = 8 # 简化统一
                break
        
        if is_root:
            root_score += current_root_score
            roots_found.append(f"{zhi}(+{current_root_score})")
    
    score += root_score
    if roots_found:
        details.append(f"通根: {', '.join(roots_found)}")
    
    # 3. 天干生扶 (排除日主自己)
    help_count = 0
    drain_count = 0
    relations = WU_XING_RELATIONS[day_element]
    
    for pillar in pillars:
        if pillar["position"] == "day":
            continue # 跳过日主
            
        gan_element = pillar["gan_element"]
        
        # 生我(印) 或 同我(比劫) = 帮扶
        if gan_element == relations["生我"] or gan_element == day_element:
            help_count += 1
            score += 10
        # 我生/克我/我克 = 耗泄
        else:
            drain_count += 1
            score -= 10
            
    if help_count > 0:
        details.append(f"天干帮扶{help_count}位(+{help_count * 10})")
    if drain_count > 0:
        details.append(f"天干耗泄{drain_count}位({drain_count * -10})")
    
    # 4. 确定强弱等级
    if score >= 50:
        level = "极强"
        level_desc = "日主极旺，多为专旺或从强"
    elif score >= 20:
        level = "偏强"
        level_desc = "日主偏旺，喜克泄耗"
    elif score >= -10:
        level = "中和"
        level_desc = "日主中和，五行流通"
    elif score >= -40:
        level = "偏弱"
        level_desc = "日主偏弱，喜生扶"
    else:
        level = "极弱"
        level_desc = "日主极弱，多为从弱或从势"
    
    return {
        "score": float(score),
        "level": level,
        "level_desc": level_desc,
        "details": details,
        "day_element": day_element
    }


def calculate_useful_gods(
    day_gan: str,
    strength_result: Dict[str, Any],
    month_zhi: str
) -> Dict[str, Any]:
    """
    计算喜用神 (P0升级版：含调候与通关)
    
    Args:
        day_gan: 日干
        strength_result: 身强弱结果
        month_zhi: 月支 (用于调候)
        
    Returns:
        喜用忌神结果
    """
    day_element = WU_XING[day_gan]
    level = strength_result["level"]
    relations = WU_XING_RELATIONS[day_element]
    
    xi_shen = []
    yong_shen = None # 最主要用神
    ji_shen = []
    xian_shen = []
    
    # === 1. 扶抑用神 (基础) ===
    if level in ["极强", "偏强"]:
        # 身强喜: 克(官杀), 泄(食伤), 耗(财)
        # 优先取用原则: 
        # 极强(专旺/从强) -> 顺势而为, 喜印比
        if level == "极强": # 特殊处理: 假定为专旺
             yong_shen = relations["同我"] # 用比劫
             xi_shen = [relations["生我"], relations["同我"]]
             ji_shen = [relations["克我"], relations["我克"]] # 忌财官
        else:
             # 偏强 -> 抑之
             # 官杀首选 (克), 食伤次之 (泄), 财星 (耗)
             yong_shen = relations["克我"] 
             xi_shen = [relations["克我"], relations["我生"], relations["我克"]]
             ji_shen = [relations["生我"], relations["同我"]] # 忌印比

    elif level in ["极弱", "偏弱"]:
        if level == "极弱": # 特殊处理: 假定为从格(从弱/从杀/从财)
             # 顺势而为 -> 喜克泄耗, 忌印比
             yong_shen = relations["克我"] # 假定从杀/从势
             xi_shen = [relations["克我"], relations["我生"], relations["我克"]]
             ji_shen = [relations["生我"], relations["同我"]]
        else:
             # 偏弱 -> 扶之
             yong_shen = relations["生我"] # 此时印星最有力
             xi_shen = [relations["生我"], relations["同我"]]
             ji_shen = [relations["克我"], relations["我生"], relations["我克"]] # 忌官杀食伤财
             
    else: # 中和
        # 通关为主, 追求平衡
        yong_shen = relations["我生"] # 食伤流通
        xi_shen = [relations["我生"], relations["我克"]]
        ji_shen = []
    
    # === 2. 调候用神 (气候调整) ===
    # 冬月 (亥子丑) -> 寒冷 -> 喜火暖局
    # 夏月 (巳午未) -> 炎热 -> 喜水润局
    tiao_hou = None
    
    if month_zhi in ["亥", "子", "丑"]:
        # 冬生人, 无论身强弱, 局中要有火
        if "火" not in xi_shen:
            xi_shen.append("火")
            # 如果用神不是火, 则火为重要辅助
            if yong_shen != "火":
                tiao_hou = "火 (调候)"
                
    elif month_zhi in ["巳", "午", "未"]:
        # 夏生人, 局中要有水
         if "水" not in xi_shen:
            xi_shen.append("水")
            if yong_shen != "水":
                tiao_hou = "水 (调候)"
                
    # === 3. 通关用神 (简单逻辑) ===
    # 比如: 金木交战 (金克木), 用水通关 (金生水, 水生木)
    tong_guan = None
    # 暂略复杂判定, 仅作为概念预留
    
    # 去重
    xi_shen = list(set(xi_shen))
    ji_shen = list(set(ji_shen))
    
    # 确保忌神里没有喜神 (调候优先)
    ji_shen = [e for e in ji_shen if e not in xi_shen]
    
    # 构造返回
    return {
        "yong_shen": yong_shen,
        "xi_shen": xi_shen,
        "ji_shen": ji_shen,
        "xian_shen": xian_shen,
        "tiao_hou": tiao_hou,
        "tong_guan": tong_guan
    }


def determine_pattern(
    day_gan: str,
    month_zhi: str,
    pillars: List[Dict[str, Any]],
    strength_result: Dict[str, Any]
) -> Dict[str, Any]:
    """
    判断命局格局 (P0升级版：涵盖正格与特殊格局)
    
    Args:
        day_gan: 日干
        month_zhi: 月支
        pillars: 四柱数据
        strength_result: 身强弱结果
        
    Returns:
        格局判断结果
    """
    score = strength_result["score"]
    level = strength_result["level"]
    day_element = WU_XING[day_gan]
    
    patterns = []
    main_pattern = None
    
    # === 1. 特殊格局判断 (优先) ===
    # 1.1 专旺格 (身极强)
    if level == "极强" and score >= 60: # 提高门槛
        # 检查是否五行单一
        patterns.append({
            "name": f"{day_element}专旺格",
            "type": "外格",
            "revealed": True,
            "desc": f"日主极旺，气势专一于{day_element}，顺势而为"
        })
        
    # 1.2 从格 (身极弱)
    elif level == "极弱" and score <= -40:
        # 判断从什么
        # 统计最强势力
        elements_count = {"木": 0, "火": 0, "土": 0, "金": 0, "水": 0}
        for p in pillars:
            elements_count[p["gan_element"]] += 1
            elements_count[p["zhi_element"]] += 1
            
        # 排除日干自己
        elements_count[day_element] -= 1
        
        dominant_element = max(elements_count, key=elements_count.get)
        dominant_ten_god = get_ten_god(day_gan, dominant_element) # 这里需要一个简化的十神查找
        
        # 简单的十神反查
        relations = WU_XING_RELATIONS[day_element]
        pattern_name = "从弱格"
        if dominant_element == relations["克我"]:
            pattern_name = "从杀格"
        elif dominant_element == relations["我克"]:
            pattern_name = "从财格"
        elif dominant_element == relations["我生"]:
            pattern_name = "从儿格"
            
        patterns.append({
            "name": pattern_name,
            "type": "外格",
            "revealed": True,
            "desc": f"日主极弱，势从{dominant_element}，为{pattern_name}"
        })

    # === 2. 正格判断 (月令藏干) ===
    # 月支藏干取格
    month_hidden = ZHI_CANG_GAN.get(month_zhi, [])
    
    # 建禄格/羊刃格 (月令为比劫)
    month_initial = month_hidden[0]
    initial_element = WU_XING[month_initial]
    
    if initial_element == day_element:
        # 比肩=建禄, 劫财=羊刃
        ten_god = get_ten_god(day_gan, month_initial)
        name = "建禄格" if ten_god == "比肩" else "羊刃格"
        patterns.append({
            "name": name,
            "type": "正格",
            "revealed": True,
            "desc": f"月令{month_zhi}为日主之{ten_god}"
        })
    else:
        # 正常取格 (看透干)
        found_zheng_ge = False
        for stem in month_hidden:
            ten_god = get_ten_god(day_gan, stem)
            if ten_god in ["比肩", "劫财"]: continue # 比劫不取正格
            
            # 检查透干
            is_revealed = any(p["gan"] == stem for p in pillars)
            pattern_name = f"{ten_god}格"
            
            p_data = {
                "name": pattern_name,
                "type": "正格",
                "revealed": is_revealed,
                "desc": f"月支藏{stem}({ten_god}){'透干' if is_revealed else '未透'}"
            }
            
            if is_revealed:
                patterns.insert(0, p_data) # 透干优先
                found_zheng_ge = True
            else:
                patterns.append(p_data)
    
    # 取最显著的格局
    if patterns:
        main_pattern = patterns[0]
    
    return {
        "main_pattern": main_pattern,
        "all_patterns": patterns,
        "strength_level": strength_result["level"]
    }


def calculate_liunian_events(ln_gan_zhi: str, pillars: List[Dict]) -> List[str]:
    """计算流年与四柱的刑冲合害关系"""
    events = []
    if not pillars:
        return events
        
    ln_gan = ln_gan_zhi[0]
    ln_zhi = ln_gan_zhi[1]
    
    # 简单的地支关系映射
    # 六冲
    LIU_CHONG = {'子': '午', '丑': '未', '寅': '申', '卯': '酉', '辰': '戌', '巳': '亥',
                 '午': '子', '未': '丑', '申': '寅', '酉': '卯', '戌': '辰', '亥': '巳'}
    # 六合
    LIU_HE = {'子': '丑', '丑': '子', '寅': '亥', '亥': '寅', '卯': '戌', '戌': '卯', 
              '辰': '酉', '酉': '辰', '巳': '申', '申': '巳', '午': '未', '未': '午'}
    
    # 检查与日柱的关系 (最重要)
    day_pillar = next((p for p in pillars if p['position'] == 'day'), None)
    if day_pillar:
        day_zhi = day_pillar['zhi']
        day_gan = day_pillar['gan']
        
        # 伏吟 (天地同)
        if ln_gan_zhi == day_pillar['gan_zhi']:
            events.append("日柱伏吟")
        # 反吟 (天克地冲 - 简易版仅看地支冲)
        elif LIU_CHONG.get(ln_zhi) == day_zhi:
            events.append("日支相冲")
        elif LIU_HE.get(ln_zhi) == day_zhi:
            events.append("日支相合")
            
    # 检查与年柱 (太岁)
    year_pillar = next((p for p in pillars if p['position'] == 'year'), None)
    if year_pillar:
        year_zhi = year_pillar['zhi']
        if ln_gan_zhi == year_pillar['gan_zhi']:
            events.append("本命年")
        elif LIU_CHONG.get(ln_zhi) == year_zhi:
            events.append("冲太岁")
        elif LIU_HE.get(ln_zhi) == year_zhi:
            events.append("合太岁")

    return events

def get_da_yun(
    solar: Solar,
    gender: int,
    day_gan: str,
    pillars: List[Dict] = None
) -> List[Dict[str, Any]]:
    """
    计算大运及流年
    
    Args:
        solar: 阳历对象
        gender: 1男 0女
        day_gan: 日干 (用于推算流年十神)
        pillars: 四柱数据 (用于计算流年事件)
        
    Returns:
        大运列表
    """
    lunar = solar.getLunar()
    eight_char = lunar.getEightChar()
    
    # 阳男阴女顺推，阴男阳女逆推
    # lunar-python 库已经封装了逻辑
    yun = eight_char.getYun(gender)
    
    da_yun_list = []
    
    # 获取大运
    # getDaYun returns array of DaYun objects
    dys = yun.getDaYun()
    
    for i, dy in enumerate(dys):
        if dy.getIndex() == 0:
            # 跳过起运前的童限
            continue
            
        start_year = dy.getStartYear()
        start_age = dy.getStartAge()
        end_year = dy.getEndYear()
        
        # 计算该大运内的10年流年
        years = []
        # getLiuNian returns a list of 10 objects
        liu_nian_list = dy.getLiuNian()
        
        for ln in liu_nian_list:
            current_year = ln.getYear()
            current_age = ln.getAge()
            gan_zhi = ln.getGanZhi()
            gan = gan_zhi[0] # 流年天干           
            # 计算流年十神 (相对于日主)
            ten_god = get_ten_god(day_gan, gan)
            
            # 计算流年事件
            events = calculate_liunian_events(gan_zhi, pillars) if pillars else []
            
            years.append({
                "year": current_year,
                "age": current_age,
                "gan_zhi": gan_zhi,
                "ten_god": ten_god,
                "events": events
            })
            
        da_yun_list.append({
            "index": dy.getIndex(),
            "start_age": start_age,
            "end_age": dy.getEndAge(),
            "start_year": start_year,
            "end_year": end_year,
            "gan_zhi": dy.getGanZhi(),
            "years": years
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
    da_yun = get_da_yun(solar, gender, day_gan, pillars)
    
    # 五行统计
    elements_count = {"木": 0, "火": 0, "土": 0, "金": 0, "水": 0}
    for pillar in pillars:
        elements_count[pillar["gan_element"]] += 1
        elements_count[pillar["zhi_element"]] += 1
    
    # === 新增分析功能 ===
    # 身强身弱
    strength_analysis = calculate_day_master_strength(day_gan, month_zhi, pillars)
    
    # 喜用神
    useful_gods = calculate_useful_gods(day_gan, strength_analysis, month_zhi)
    
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

