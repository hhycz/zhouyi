# 周易卜卦系统 - 项目上下文

> 此文档用于跨会话保持项目状态和上下文，防止AI"失忆"。
> 最后更新: 2025-12-15

## 项目概述

基于周易的智能卜卦系统，融合传统玄学与现代AI技术，提供沉浸式的人机交互体验。

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Vue 3 + TypeScript + Vite |
| 后端 | Python 3.12 + FastAPI + Uvicorn |
| AI | Google Gemini API (gemma-3-1b-it) |
| 历法 | lunar-python |

## 目录结构

```
zhouyi-divination/
├── backend/
│   ├── app/
│   │   ├── routers/divination.py     # API路由
│   │   ├── services/
│   │   │   ├── bazi_service.py       # 八字排盘
│   │   │   ├── liuyao_service.py     # 六爻金钱卦
│   │   │   ├── interpretation_service.py  # 卦辞解读
│   │   │   └── gemini_service.py     # AI解卦
│   │   └── data/hexagram_texts.json  # 卦辞数据库
│   ├── .env                          # API密钥配置
│   └── venv/                         # Python虚拟环境
└── frontend/
    └── src/
        ├── components/
        │   ├── chat/ChatContainer.vue    # 主对话界面
        │   ├── widgets/
        │   │   ├── BreathGuide.vue       # 净心呼吸引导
        │   │   ├── CoinToss.vue          # 抛币动画
        │   │   └── ...
        │   ├── results/
        │   │   ├── BaziChart.vue         # 八字排盘展示
        │   │   └── LiuyaoChart.vue       # 六爻卦象展示
        │   └── background/
        │       └── MysticalBackground.vue # 神秘背景动画
        └── api/index.ts                  # API客户端
```

## 已完成功能 ✅

### 核心功能
- [x] 八字排盘（四柱、藏干、十神、大运）
- [x] 真太阳时校正（经纬度+时差方程）
- [x] 六爻金钱卦（64卦、六兽、世应、变卦）
- [x] 卦辞数据库（8卦完成，含卦辞+爻辞）
- [x] AI智能解卦（Gemini API集成）

### 交互体验
- [x] 对话式引导流程
- [x] 净心呼吸引导动画（3次深呼吸）
- [x] 抛币3D动画效果
- [x] 神秘周易风格背景（八卦阵+太极+星辰）

## 待开发功能 🚧

- [ ] 补充完整64卦爻辞数据
- [ ] 梅花易数起卦
- [ ] 紫微斗数
- [ ] 用户账号与命书存储
- [ ] 合盘分析

## 配置信息

### 端口
- 前端: http://localhost:3000
- 后端: http://localhost:8000

### 环境变量
```bash
# backend/.env
GEMINI_API_KEY=
```

## 启动命令

```bash
# 后端
cd backend && source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000

# 前端
cd frontend && npm run dev
```

## 重要备注

1. Gemini API使用 `gemma-3-1b-it` 模型（无配额限制）
2. 卦辞数据在 `backend/app/data/hexagram_texts.json`
3. 前端API调用基础URL为 `http://localhost:8000/api`

## GitHub 同步规范

> ⚠️ **重要**: 每次更新代码时必须同步更新此备忘录！

### 仓库地址
- GitHub: https://github.com/hhycz/zhouyi

### 同步要求
1. **代码变更时**: 同步更新本文档的相关章节
2. **功能完成时**: 更新 "已完成功能" 列表，将 `[ ]` 改为 `[x]`
3. **新增待办时**: 在 "待开发功能" 列表添加新项目
4. **卦辞更新时**: 记录已完成的卦辞数量
5. **配置变更时**: 更新 "配置信息" 相关内容

### 提交规范
```bash
# 更新代码时务必包含备忘录
git add .agent/PROJECT_CONTEXT.md
git commit -m "docs: 更新项目上下文备忘录"
git push origin main
```

### 更新日期
每次更新备忘录时，同步更新文档顶部的 "最后更新" 日期。
