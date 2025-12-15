"""
六爻排盘服务
Liuyao (Six Lines) Divination Service
"""
from typing import Dict, Any, List, Tuple
import random


# 八卦基本信息
BAGUA = {
    "乾": {"symbol": "☰", "nature": "天", "direction": "西北", "element": "金", "lines": [1, 1, 1]},
    "兑": {"symbol": "☱", "nature": "泽", "direction": "西", "element": "金", "lines": [0, 1, 1]},
    "离": {"symbol": "☲", "nature": "火", "direction": "南", "element": "火", "lines": [1, 0, 1]},
    "震": {"symbol": "☳", "nature": "雷", "direction": "东", "element": "木", "lines": [0, 0, 1]},
    "巽": {"symbol": "☴", "nature": "风", "direction": "东南", "element": "木", "lines": [1, 1, 0]},
    "坎": {"symbol": "☵", "nature": "水", "direction": "北", "element": "水", "lines": [0, 1, 0]},
    "艮": {"symbol": "☶", "nature": "山", "direction": "东北", "element": "土", "lines": [1, 0, 0]},
    "坤": {"symbol": "☷", "nature": "地", "direction": "西南", "element": "土", "lines": [0, 0, 0]},
}

# 64卦名称索引 (上卦, 下卦) -> 卦名
HEXAGRAMS = {
    ("乾", "乾"): "乾为天", ("坤", "乾"): "地天泰", ("坎", "乾"): "水天需", ("离", "乾"): "火天大有",
    ("震", "乾"): "雷天大壮", ("巽", "乾"): "风天小畜", ("艮", "乾"): "山天大畜", ("兑", "乾"): "泽天夬",
    ("乾", "坤"): "天地否", ("坤", "坤"): "坤为地", ("坎", "坤"): "水地比", ("离", "坤"): "火地晋",
    ("震", "坤"): "雷地豫", ("巽", "坤"): "风地观", ("艮", "坤"): "山地剥", ("兑", "坤"): "泽地萃",
    ("乾", "坎"): "天水讼", ("坤", "坎"): "地水师", ("坎", "坎"): "坎为水", ("离", "坎"): "火水未济",
    ("震", "坎"): "雷水解", ("巽", "坎"): "风水涣", ("艮", "坎"): "山水蒙", ("兑", "坎"): "泽水困",
    ("乾", "离"): "天火同人", ("坤", "离"): "地火明夷", ("坎", "离"): "水火既济", ("离", "离"): "离为火",
    ("震", "离"): "雷火丰", ("巽", "离"): "风火家人", ("艮", "离"): "山火贲", ("兑", "离"): "泽火革",
    ("乾", "震"): "天雷无妄", ("坤", "震"): "地雷复", ("坎", "震"): "水雷屯", ("离", "震"): "火雷噬嗑",
    ("震", "震"): "震为雷", ("巽", "震"): "风雷益", ("艮", "震"): "山雷颐", ("兑", "震"): "泽雷随",
    ("乾", "巽"): "天风姤", ("坤", "巽"): "地风升", ("坎", "巽"): "水风井", ("离", "巽"): "火风鼎",
    ("震", "巽"): "雷风恒", ("巽", "巽"): "巽为风", ("艮", "巽"): "山风蛊", ("兑", "巽"): "泽风大过",
    ("乾", "艮"): "天山遁", ("坤", "艮"): "地山谦", ("坎", "艮"): "水山蹇", ("离", "艮"): "火山旅",
    ("震", "艮"): "雷山小过", ("巽", "艮"): "风山渐", ("艮", "艮"): "艮为山", ("兑", "艮"): "泽山咸",
    ("乾", "兑"): "天泽履", ("坤", "兑"): "地泽临", ("坎", "兑"): "水泽节", ("离", "兑"): "火泽睽",
    ("震", "兑"): "雷泽归妹", ("巽", "兑"): "风泽中孚", ("艮", "兑"): "山泽损", ("兑", "兑"): "兑为泽",
}

# 六兽
SIX_BEASTS = ["青龙", "朱雀", "勾陈", "螣蛇", "白虎", "玄武"]

# 六亲 (以日干为主)
SIX_RELATIVES = {
    "生我": "父母",
    "我生": "子孙", 
    "克我": "官鬼",
    "我克": "妻财",
    "同我": "兄弟"
}


def simulate_coin_toss() -> int:
    """
    模拟抛三枚铜钱
    
    返回值:
    - 6: 老阴 (三反) ⚋ 变爻
    - 7: 少阳 (二反一正) ⚊
    - 8: 少阴 (二正一反) ⚋
    - 9: 老阳 (三正) ⚊ 变爻
    
    正面(花纹)=3, 反面(字)=2
    """
    coins = [random.choice([2, 3]) for _ in range(3)]
    return sum(coins)


def coin_result_to_yao(value: int) -> Dict[str, Any]:
    """
    将铜钱结果转换为爻的信息
    """
    yao_info = {
        6: {"type": "yin", "changing": True, "symbol": "⚋", "name": "老阴", "value": 0},
        7: {"type": "yang", "changing": False, "symbol": "⚊", "name": "少阳", "value": 1},
        8: {"type": "yin", "changing": False, "symbol": "⚋", "name": "少阴", "value": 0},
        9: {"type": "yang", "changing": True, "symbol": "⚊", "name": "老阳", "value": 1},
    }
    return yao_info.get(value, yao_info[7])


def lines_to_trigram(lines: List[int]) -> str:
    """
    根据三个爻值找到对应的卦名
    """
    for name, info in BAGUA.items():
        if info["lines"] == lines:
            return name
    return "乾"


def get_hexagram_name(upper: str, lower: str) -> str:
    """
    根据上下卦获取64卦名称
    """
    return HEXAGRAMS.get((upper, lower), f"{upper}{lower}卦")


def calculate_world_response(hexagram_lines: List[int]) -> Tuple[int, int]:
    """
    安世应
    
    根据卦的结构确定世爻和应爻的位置
    简化算法: 根据上下卦的关系计算
    """
    # 简化处理: 世爻在初爻到六爻之间,应爻与世爻相隔三位
    lower = hexagram_lines[:3]
    upper = hexagram_lines[3:]
    
    # 计算变化位置
    diff_count = sum(1 for i in range(3) if lower[i] != upper[i])
    
    world_positions = {0: 6, 1: 1, 2: 2, 3: 3}
    world = world_positions.get(diff_count, 4)
    response = (world + 2) % 6 + 1 if world <= 3 else (world - 2) if world > 3 else 4
    
    return world, response


def generate_liuyao_chart(
    coin_results: List[int] = None,
    question: str = ""
) -> Dict[str, Any]:
    """
    生成六爻卦象
    
    Args:
        coin_results: 六次抛币结果 [6-9], 如果为None则自动模拟
        question: 所问之事
        
    Returns:
        完整的卦象数据
    """
    # 如果没有提供结果,自动模拟
    if coin_results is None:
        coin_results = [simulate_coin_toss() for _ in range(6)]
    
    # 确保有6个结果
    if len(coin_results) != 6:
        coin_results = [simulate_coin_toss() for _ in range(6)]
    
    # 解析每一爻
    yaos = []
    original_lines = []
    changed_lines = []
    moving_positions = []
    
    for i, result in enumerate(coin_results):
        yao = coin_result_to_yao(result)
        yao["position"] = i + 1
        yao["position_name"] = ["初爻", "二爻", "三爻", "四爻", "五爻", "上爻"][i]
        yao["coin_value"] = result
        yaos.append(yao)
        
        original_lines.append(yao["value"])
        
        # 计算变爻后的值
        if yao["changing"]:
            moving_positions.append(i + 1)
            changed_lines.append(1 - yao["value"])  # 阴阳互换
        else:
            changed_lines.append(yao["value"])
    
    # 确定上下卦
    lower_trigram = lines_to_trigram(original_lines[:3])
    upper_trigram = lines_to_trigram(original_lines[3:])
    
    # 本卦
    original_hexagram = {
        "name": get_hexagram_name(upper_trigram, lower_trigram),
        "upper": upper_trigram,
        "lower": lower_trigram,
        "upper_symbol": BAGUA[upper_trigram]["symbol"],
        "lower_symbol": BAGUA[lower_trigram]["symbol"],
        "lines": original_lines
    }
    
    # 变卦 (如果有动爻)
    changed_hexagram = None
    if moving_positions:
        changed_lower = lines_to_trigram(changed_lines[:3])
        changed_upper = lines_to_trigram(changed_lines[3:])
        changed_hexagram = {
            "name": get_hexagram_name(changed_upper, changed_lower),
            "upper": changed_upper,
            "lower": changed_lower,
            "upper_symbol": BAGUA[changed_upper]["symbol"],
            "lower_symbol": BAGUA[changed_lower]["symbol"],
            "lines": changed_lines
        }
    
    # 安世应
    world_pos, response_pos = calculate_world_response(original_lines)
    
    # 安六兽 (简化: 从初爻开始依次安)
    for i, yao in enumerate(yaos):
        yao["beast"] = SIX_BEASTS[i]
        yao["is_world"] = (i + 1) == world_pos
        yao["is_response"] = (i + 1) == response_pos
    
    return {
        "question": question,
        "coin_results": coin_results,
        "yaos": yaos,
        "original_hexagram": original_hexagram,
        "changed_hexagram": changed_hexagram,
        "moving_positions": moving_positions,
        "world_position": world_pos,
        "response_position": response_pos,
        "interpretation_hint": _get_interpretation_hint(original_hexagram["name"], moving_positions)
    }


def _get_interpretation_hint(hexagram_name: str, moving_positions: List[int]) -> str:
    """
    生成解卦提示
    """
    if not moving_positions:
        return "六爻皆静，以卦辞断之。"
    elif len(moving_positions) == 1:
        return f"一爻变动，以第{moving_positions[0]}爻爻辞为主。"
    elif len(moving_positions) == 2:
        return "二爻变动，以上爻爻辞为主。"
    elif len(moving_positions) == 3:
        return "三爻变动，本卦与变卦卦辞参看。"
    elif len(moving_positions) == 4:
        return "四爻变动，以变卦不变之爻爻辞为主。"
    elif len(moving_positions) == 5:
        return "五爻变动，以变卦不变之爻爻辞为主。"
    else:
        return "六爻皆变，用变卦卦辞断之。"
