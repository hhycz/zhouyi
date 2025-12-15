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



async def generate_bazi_year_analysis(chart_data: Dict, target_year: int) -> Dict[str, Any]:
    """
    生成指定流年的命理分析
    """
    if not init_gemini():
        return {
            "success": False,
            "error": "Gemini API key not configured",
            "content": None
        }
        
    # 提取关键信息构建Prompt
    day_master = chart_data['chart']['day_master']['gan']
    pattern = chart_data['pattern_analysis']['main_pattern']['name']
    strong_weak = chart_data['strength_analysis']['level']
    useful_gods = chart_data['useful_gods']['yong_shen']
    xi_shen = chart_data['useful_gods']['xi_shen']
    
    # 找到该流年的信息
    year_info = None
    luck_cycle = None
    
    for cycle in chart_data.get('luck_cycles', []):
        if cycle['start_year'] <= target_year <= cycle['end_year']:
            luck_cycle = cycle
            for y in cycle.get('years', []):
                if y['year'] == target_year:
                    year_info = y
                    break
            break
            
    if not year_info:
        return {"success": False, "error": f"找不到{target_year}年的流年数据", "content": None}

    # 提取流年干支的详细信息
    ln_gan = year_info['gan_zhi'][0]
    ln_zhi = year_info['gan_zhi'][1]
    
    # 地支对应的五行和生肖
    ZHI_WUXING = {'子': '水', '丑': '土', '寅': '木', '卯': '木', '辰': '土', '巳': '火',
                  '午': '火', '未': '土', '申': '金', '酉': '金', '戌': '土', '亥': '水'}
    ZHI_SHENGXIAO = {'子': '鼠', '丑': '牛', '寅': '虎', '卯': '兔', '辰': '龙', '巳': '蛇',
                    '午': '马', '未': '羊', '申': '猴', '酉': '鸡', '戌': '狗', '亥': '猪'}
    
    ln_zhi_wx = ZHI_WUXING.get(ln_zhi, '')
    ln_shengxiao = ZHI_SHENGXIAO.get(ln_zhi, '')

    prompt = f"""
    请根据以下八字命盘，详细分析【{target_year}年】的流年运势。

    ⚠️ 重要：本年流年干支为【{year_info['gan_zhi']}】（{ln_shengxiao}年，{ln_zhi}{ln_zhi_wx}），请严格按照此信息分析，不要使用其他干支！

    【命主信息】
    日主：{day_master} ({strong_weak})
    格局：{pattern}
    喜用神：{useful_gods} (喜: {', '.join(xi_shen)})

    【当前大运】
    {luck_cycle['gan_zhi']}大运 ({luck_cycle['start_year']}~{luck_cycle['end_year']})

    【{target_year}年流年信息】
    干支：{year_info['gan_zhi']}（{ln_gan}{ln_zhi}，{ln_shengxiao}年）
    流年天干：{ln_gan}
    流年地支：{ln_zhi}（{ln_zhi_wx}）
    流年十神：{year_info['ten_god']}
    流年神煞/事件：{', '.join(year_info.get('events', [])) if year_info.get('events') else '无特殊冲合'}

    【分析要求】
    1. **吉凶判断**：结合{year_info['gan_zhi']}流年干支与命局的关系，综合判断运势得分(0-100)。
    2. **重点领域**：分析事业、财运、感情、健康中哪一方面最受影响。
    3. **关键事件**：根据流年十神（{year_info['ten_god']}）预测可能发生的事情。
    4. **趋吉避凶**：给出具体的行动建议。

    请保持语气专业、客观，使用正确的流年干支【{year_info['gan_zhi']}】进行分析。
    """

    try:
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

# Previous sync function...
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
