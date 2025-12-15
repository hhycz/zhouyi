# 周易占卜系统 | Zhouyi Divination System

一个现代化的周易占卜系统，融合传统易学智慧与现代AI技术。

## ✨ 特性

### 📚 完整的64卦数据
- 包含完整的六十四卦数据
- 每卦包含：卦辞、彖辞、象辞、六爻爻辞及详细解释
- 支持八宫卦序和传统排列

### 🎲 占卜功能
- **三枚铜钱法**：传统的掷铜钱占卜方式
- **六爻占卜**：完整的六爻起卦系统，包含世应、六兽、六亲等要素
- **八字排盘**：基于出生时间的八字分析

### 🤖 AI辅助解读
- 集成 Google Gemini AI
- 智能解读卦象含义
- 结合用户问题提供个性化建议

### 🎨 神秘主义UI设计
- 深色主题，营造神秘氛围
- 动态八卦背景动画
- 太极图、五行元素等传统符号
- 流畅的打字机效果和过渡动画

## 🏗️ 技术栈

### 后端
- **FastAPI**: 高性能 Python Web 框架
- **Python 3.9+**: 核心编程语言
- **Pydantic**: 数据验证和设置管理
- **Google Generative AI**: AI 辅助解读

### 前端
- **Vue 3**: 渐进式 JavaScript 框架
- **TypeScript**: 类型安全
- **Vite**: 快速构建工具
- **CSS3**: 自定义动画和样式

## 📦 项目结构

```
zhouyi-divination/
├── backend/                # 后端服务
│   ├── app/
│   │   ├── data/          # 64卦数据文件
│   │   ├── models/        # 数据模型
│   │   ├── routers/       # API路由
│   │   └── services/      # 业务逻辑
│   └── requirements.txt    # Python依赖
├── frontend/               # 前端应用
│   ├── src/
│   │   ├── components/    # Vue组件
│   │   ├── api/          # API调用
│   │   └── types/        # TypeScript类型
│   └── package.json       # Node依赖
└── README.md
```

## 🚀 快速开始

### 前置要求
- Python 3.9+
- Node.js 16+
- npm 或 yarn

### 后端启动

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 前端启动

```bash
cd frontend
npm install
npm run dev
```

访问 `http://localhost:5173` 即可使用系统。

## 🔑 环境配置

创建 `.env` 文件并配置以下变量：

```env
# Google Gemini API Key（可选，用于AI解读）
GOOGLE_API_KEY=your_api_key_here
```

## 📖 使用说明

1. **选择占卜类型**：六爻、八字或简单占卜
2. **输入问题**：描述你想要占卜的事项
3. **掷铜钱/输入信息**：进行占卜操作
4. **查看结果**：系统会显示卦象及详细解读
5. **AI辅助**：可选择使用AI获得更深入的分析

## 📊 数据来源

- 卦辞、彖辞、象辞：源自《周易》原文
- 爻辞解释：结合传统注疏和现代理解
- 六爻体系：基于传统六爻占卜理论

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

本项目仅供学习交流使用。

## ⚠️ 免责声明

本系统仅作为易学文化的传播和学习工具，占卜结果仅供参考。请理性对待，不要迷信。重要决策应基于理性分析和科学判断。

---

**注意**：使用 AI 解读功能需要有效的 Google Gemini API Key。
