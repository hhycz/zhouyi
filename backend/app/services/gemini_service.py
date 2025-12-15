"""
Gemini AI 解卦服务
AI-powered Hexagram Interpretation using Google Gemini
"""
import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv
import google.generativeai as genai

# 加载环境变量
load_dotenv()

# Gemini API 配置
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# 初始化 Gemini
def init_gemini():
    """初始化 Gemini API"""
    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
        return True
    return False


# 解卦系统提示词
INTERPRETATION_SYSTEM_PROMPT = """你是一位精通周易的智慧长者，融合古典智慧与现代心理学。你的风格是：
- 语言古雅但不晦涩，既有古风韵味又通俗易懂
- 解卦直指要害，不绕弯子
- 既讲传统卦理，也结合现代生活场景
- 给予积极引导，但不回避困难

解卦原则：
1. 无动爻：以本卦卦辞为主
2. 一个动爻：以该爻爻辞为主
3. 两个动爻：以上爻爻辞为主，下爻为辅
4. 三个动爻：以本卦卦辞为主，参考动爻
5. 四个动爻：以两个静爻爻辞为主（下爻为主）
6. 五个动爻：以静爻爻辞为主
7. 六爻皆动：乾坤看用九用六，其他看变卦

请用以下格式回答：
【卦象】简要说明本卦含义
【断语】针对问题的核心判断（一两句话）
【解析】详细分析（2-3段）
【建议】具体可行的行动建议
"""


async def generate_ai_interpretation(
    question: str,
    hexagram_name: str,
    changed_hexagram_name: Optional[str] = None,
    moving_positions: list = None,
    yaos_data: list = None,
    interpretation_data: Dict = None
) -> Dict[str, Any]:
    """
    使用 Gemini 生成 AI 解卦
    
    Args:
        question: 所问之事
        hexagram_name: 本卦名称
        changed_hexagram_name: 变卦名称
        moving_positions: 动爻位置列表
        yaos_data: 六爻详细数据
        interpretation_data: 基础解读数据（卦辞等）
        
    Returns:
        AI 生成的解读
    """
    if not init_gemini():
        return {
            "success": False,
            "error": "Gemini API key not configured",
            "content": None
        }
    
    moving_positions = moving_positions or []
    
    # 构建提示词
    prompt = _build_interpretation_prompt(
        question=question,
        hexagram_name=hexagram_name,
        changed_hexagram_name=changed_hexagram_name,
        moving_positions=moving_positions,
        yaos_data=yaos_data,
        interpretation_data=interpretation_data
    )
    
    try:
        # 调用 Gemini API (Gemma 模型不支持 system_instruction，合并到 prompt)
        model = genai.GenerativeModel(model_name="gemma-3-1b-it")
        
        full_prompt = INTERPRETATION_SYSTEM_PROMPT + "\n\n" + prompt
        response = await model.generate_content_async(full_prompt)
        
        return {
            "success": True,
            "error": None,
            "content": response.text
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "content": None
        }


def _build_interpretation_prompt(
    question: str,
    hexagram_name: str,
    changed_hexagram_name: Optional[str],
    moving_positions: list,
    yaos_data: list = None,
    interpretation_data: Dict = None
) -> str:
    """构建解卦提示词"""
    
    parts = []
    
    # 问题
    parts.append(f"【所问之事】{question if question else '未说明'}")
    
    # 卦象信息
    parts.append(f"【本卦】{hexagram_name}")
    
    if changed_hexagram_name and changed_hexagram_name != hexagram_name:
        parts.append(f"【变卦】{changed_hexagram_name}")
    
    # 动爻信息
    if moving_positions:
        yao_names = {1: "初爻", 2: "二爻", 3: "三爻", 4: "四爻", 5: "五爻", 6: "上爻"}
        moving_str = "、".join([yao_names.get(p, f"{p}爻") for p in moving_positions])
        parts.append(f"【动爻】{moving_str}变动")
    else:
        parts.append("【动爻】无动爻")
    
    # 卦辞信息（如果有）
    if interpretation_data:
        orig = interpretation_data.get("original_hexagram", {})
        if orig:
            if orig.get("guaCi"):
                parts.append(f"【卦辞】{orig.get('guaCi')}")
            if orig.get("xiangCi"):
                parts.append(f"【象辞】{orig.get('xiangCi')}")
        
        # 动爻爻辞
        moving_yaos = interpretation_data.get("moving_yaos", [])
        for yao in moving_yaos:
            parts.append(f"【{yao.get('text', '')}】{yao.get('explain', '')}")
    
    parts.append("\n请根据以上卦象，为问卦者解读。")
    
    return "\n".join(parts)


# 同步版本（用于不支持异步的场景）
def generate_ai_interpretation_sync(
    question: str,
    hexagram_name: str,
    changed_hexagram_name: Optional[str] = None,
    moving_positions: list = None,
    yaos_data: list = None,
    interpretation_data: Dict = None
) -> Dict[str, Any]:
    """同步版本的 AI 解卦"""
    
    if not init_gemini():
        return {
            "success": False,
            "error": "Gemini API key not configured",
            "content": None
        }
    
    moving_positions = moving_positions or []
    
    prompt = _build_interpretation_prompt(
        question=question,
        hexagram_name=hexagram_name,
        changed_hexagram_name=changed_hexagram_name,
        moving_positions=moving_positions,
        yaos_data=yaos_data,
        interpretation_data=interpretation_data
    )
    
    try:
        model = genai.GenerativeModel(model_name="gemma-3-1b-it")
        
        full_prompt = INTERPRETATION_SYSTEM_PROMPT + "\n\n" + prompt
        response = model.generate_content(full_prompt)
        
        return {
            "success": True,
            "error": None,
            "content": response.text
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "content": None
        }
