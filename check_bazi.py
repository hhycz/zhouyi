import sys
import os
import sys
import os
from pprint import pprint

# 添加路径以便导入app模块
sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))

from app.services.bazi_service import generate_bazi_chart

def test_bazi_calc():
    print("Testing BaZi Calculation...")
    
    # 案例1: 2000年1月1日 12:00 (己卯年 丙子月 戊午日 戊午时)
    # 冬月土 (子月戊土), 失令 (子是水, 土克水为财, 耗气)
    # 看强弱是否偏弱
    
    result = generate_bazi_chart(2000, 1, 1, 12, 0, longitude=116.4, latitude=39.9)
    
    print("\n=== Case 1: 2000-01-01 12:00 ===")
    chart = result["chart"]
    day_master = chart["day_master"]["gan"]
    print(f"Day Master: {day_master}")
    
    strength = result["strength_analysis"]
    print(f"Strength Score: {strength['score']}")
    print(f"Level: {strength['level']}")
    print(f"Details: {strength['details']}")
    
    useful = result["useful_gods"]
    print(f"Useful Gods: {useful}")
    
    print(f"Pattern: {result['pattern_analysis']}")

    # Inspect Da Yun and Liu Nian
    print("\n=== Da Yun Details ===")
    if result['luck_cycles']:
        first_cycle = result['luck_cycles'][1] # Check 2nd cycle (skipping 1st if childhood)
        print(f"Cycle: {first_cycle['gan_zhi']} ({first_cycle['start_year']}-{first_cycle['end_year']})")
        print(f"Liu Nian count: {len(first_cycle['years'])}")
        if first_cycle['years']:
            print("First year:", first_cycle['years'][0])
            print("Events:", first_cycle['years'][0].get('events'))
    
    print("-" * 30)
    
    # 案例2: 1990年6月1日 12:00 (庚午 辛巳 丙寅 甲午)
    # 夏月火 (巳月丙火), 得令 (旺)
    # 这是一个可能的专旺或极强
    
    result2 = generate_bazi_chart(1990, 6, 1, 12, 0)
    print("\n=== Case 2: 1990-06-01 12:00 ===")
    print(f"Strength Score: {result2['strength_analysis']['score']}")
    print(f"Level: {result2['strength_analysis']['level']}")
    print(f"Tiao Hou: {result2['useful_gods'].get('tiao_hou')}")


if __name__ == "__main__":
    test_bazi_calc()
