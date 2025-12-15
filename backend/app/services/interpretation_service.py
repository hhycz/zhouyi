"""
解卦服务
Hexagram Interpretation Service
"""
import json
import os
from typing import Dict, Any, List, Optional

# 加载卦辞数据
DATA_DIR = os.path.dirname(__file__).replace('/services', '/data')
HEXAGRAM_DATA: Dict = {}

def load_hexagram_data():
    """加载64卦爻辞数据"""
    global HEXAGRAM_DATA
    data_file = os.path.join(DATA_DIR, 'hexagram_texts.json')
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            HEXAGRAM_DATA = data.get('hexagrams', {})
    except FileNotFoundError:
        print(f"Warning: Hexagram data file not found: {data_file}")
        HEXAGRAM_DATA = {}
    except json.JSONDecodeError as e:
        print(f"Error parsing hexagram data: {e}")
        HEXAGRAM_DATA = {}

# 初始化加载
load_hexagram_data()


def get_hexagram_text(hexagram_name: str) -> Optional[Dict]:
    """
    获取指定卦的完整文本数据
    
    Args:
        hexagram_name: 卦名，如 "乾为天"、"水雷屯"
        
    Returns:
        卦辞数据字典，包含卦辞、爻辞等
    """
    return HEXAGRAM_DATA.get(hexagram_name)


def get_yao_text(hexagram_name: str, position: int) -> Optional[Dict]:
    """
    获取指定卦指定爻的爻辞
    
    Args:
        hexagram_name: 卦名
        position: 爻位（1-6）
        
    Returns:
        爻辞数据
    """
    hexagram = HEXAGRAM_DATA.get(hexagram_name)
    if not hexagram:
        return None
    
    yao_ci = hexagram.get('yaoCi', [])
    for yao in yao_ci:
        if yao.get('position') == position:
            return yao
    return None


def generate_interpretation(
    hexagram_name: str,
    changed_hexagram_name: Optional[str] = None,
    moving_positions: List[int] = None,
    question: str = ""
) -> Dict[str, Any]:
    """
    生成卦象解读
    
    Args:
        hexagram_name: 本卦名称
        changed_hexagram_name: 变卦名称（如有动爻）
        moving_positions: 动爻位置列表
        question: 所问之事
        
    Returns:
        解读数据，包含卦辞、爻辞解读
    """
    moving_positions = moving_positions or []
    
    result = {
        "original_hexagram": None,
        "changed_hexagram": None,
        "moving_yaos": [],
        "interpretation_summary": "",
        "advice": ""
    }
    
    # 获取本卦数据
    original = get_hexagram_text(hexagram_name)
    if original:
        result["original_hexagram"] = {
            "name": hexagram_name,
            "symbol": original.get("symbol", ""),
            "keywords": original.get("keywords", []),
            "guaCi": original.get("guaCi", ""),
            "guaCiExplain": original.get("guaCiExplain", ""),
            "xiangCi": original.get("xiangCi", "")
        }
    
    # 获取变卦数据
    if changed_hexagram_name and changed_hexagram_name != hexagram_name:
        changed = get_hexagram_text(changed_hexagram_name)
        if changed:
            result["changed_hexagram"] = {
                "name": changed_hexagram_name,
                "symbol": changed.get("symbol", ""),
                "keywords": changed.get("keywords", []),
                "guaCi": changed.get("guaCi", ""),
                "guaCiExplain": changed.get("guaCiExplain", "")
            }
    
    # 获取动爻爻辞
    for pos in moving_positions:
        yao = get_yao_text(hexagram_name, pos)
        if yao:
            result["moving_yaos"].append(yao)
    
    # 生成解读摘要
    result["interpretation_summary"] = _generate_summary(
        hexagram_name, 
        changed_hexagram_name, 
        moving_positions,
        original
    )
    
    # 生成建议
    result["advice"] = _generate_advice(original, moving_positions)
    
    return result


def _generate_summary(
    hexagram_name: str,
    changed_hexagram_name: Optional[str],
    moving_positions: List[int],
    hexagram_data: Optional[Dict]
) -> str:
    """生成解读摘要"""
    if not hexagram_data:
        return f"卦象为{hexagram_name}，详细解读数据待完善。"
    
    summary_parts = []
    
    # 卦象基本含义
    keywords = hexagram_data.get("keywords", [])
    if keywords:
        summary_parts.append(f"此卦主{' '.join(keywords[:2])}")
    
    # 卦辞解读
    gua_ci = hexagram_data.get("guaCi", "")
    if gua_ci:
        summary_parts.append(f"卦辞曰：「{gua_ci}」")
    
    # 动爻情况
    if len(moving_positions) == 0:
        summary_parts.append("六爻皆静，以本卦卦辞为主。")
    elif len(moving_positions) == 1:
        pos = moving_positions[0]
        summary_parts.append(f"第{pos}爻变动，以该爻爻辞为主。")
    elif len(moving_positions) == 6:
        summary_parts.append("六爻皆动，以变卦卦辞为主。")
    else:
        summary_parts.append(f"有{len(moving_positions)}爻变动，综合参看动爻爻辞。")
    
    # 变卦提示
    if changed_hexagram_name and changed_hexagram_name != hexagram_name:
        summary_parts.append(f"本卦变为「{changed_hexagram_name}」，示事态走向。")
    
    return " ".join(summary_parts)


def _generate_advice(hexagram_data: Optional[Dict], moving_positions: List[int]) -> str:
    """根据卦象生成建议"""
    if not hexagram_data:
        return "宜静观其变，勿轻举妄动。"
    
    xiang_ci = hexagram_data.get("xiangCi", "")
    if xiang_ci:
        return f"《象》曰：「{xiang_ci}」依此行事，自可趋吉避凶。"
    
    return "行事宜谨慎，顺应天时。"


def reload_hexagram_data():
    """重新加载卦辞数据（用于热更新）"""
    load_hexagram_data()
    return len(HEXAGRAM_DATA)
