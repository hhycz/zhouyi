<script setup lang="ts">
import { ref } from 'vue';
import { api } from '@/api';

interface Yao {
  position: number;
  position_name: string;
  type: string;
  symbol: string;
  name: string;
  changing: boolean;
  beast: string;
  is_world: boolean;
  is_response: boolean;
}

interface Hexagram {
  name: string;
  upper: string;
  lower: string;
  upper_symbol: string;
  lower_symbol: string;
  lines: number[];
}

interface Interpretation {
  original_hexagram?: {
    guaCi?: string;
    guaCiExplain?: string;
    xiangCi?: string;
    keywords?: string[];
  };
  interpretation_summary?: string;
  advice?: string;
  moving_yaos?: Array<{
    position: number;
    text: string;
    explain: string;
  }>;
}

interface LiuyaoData {
  question: string;
  yaos: Yao[];
  original_hexagram: Hexagram;
  changed_hexagram: Hexagram | null;
  moving_positions: number[];
  world_position: number;
  response_position: number;
  interpretation_hint: string;
  interpretation?: Interpretation;
}

const props = defineProps<{
  data: LiuyaoData;
}>();

const isAILoading = ref(false);
const aiContent = ref('');
const aiError = ref('');

async function requestAIInterpretation() {
  isAILoading.value = true;
  aiError.value = '';
  
  try {
    const result = await api.getAIInterpretation({
      question: props.data.question,
      hexagramName: props.data.original_hexagram.name,
      changedHexagramName: props.data.changed_hexagram?.name,
      movingPositions: props.data.moving_positions,
      interpretationData: props.data.interpretation
    });
    
    if (result.success) {
      aiContent.value = result.content;
    } else {
      aiError.value = '解卦失败，请稍后重试';
    }
  } catch (err: any) {
    aiError.value = err.response?.data?.detail || '网络错误，请检查连接';
  } finally {
    isAILoading.value = false;
  }
}

// 辅助函数：根据爻的位置计算动画延迟 (从下往上: 初爻->上爻)
// 传入 index 是数组索引，可能是倒序的显示。 data.yaos 通常是按 position 1-6 排序
// 界面上我们显示通常是 上爻在最上面 (position 6), 初爻在最下面 (position 1)
// v-for 是 [...data.yaos].reverse()，所以 index 0 是上爻 (pos 6)， index 5 是初爻 (pos 1)
// 我们希望动画顺序是 初爻 (index 5) -> ... -> 上爻 (index 0)
// delay = (5 - index) * 0.2s
function getAnimDelay(index: number) {
  return `${(5 - index) * 0.15}s`;
}
</script>

<template>
  <div class="liuyao-chart card-glow fade-in-up">
    <!-- 卦象头部 -->
    <div class="chart-header">
      <div class="hexagram-display">
        <div class="hexagram original">
          <div class="symbol-box">
             <span class="symbol-text">{{ data.original_hexagram.upper_symbol }}{{ data.original_hexagram.lower_symbol }}</span>
          </div>
          <span class="name">{{ data.original_hexagram.name }}</span>
        </div>
        <span v-if="data.changed_hexagram" class="arrow">➤</span>
        <div v-if="data.changed_hexagram" class="hexagram changed">
          <div class="symbol-box">
            <span class="symbol-text">{{ data.changed_hexagram.upper_symbol }}{{ data.changed_hexagram.lower_symbol }}</span>
          </div>
          <span class="name">{{ data.changed_hexagram.name }}</span>
        </div>
      </div>
    </div>
    
    <!-- 六爻列表 -->
    <div class="yaos-container">
      <div 
        v-for="(yao, index) in [...data.yaos].reverse()" 
        :key="yao.position"
        class="yao-row"
        :class="{ 
          changing: yao.changing,
          world: yao.is_world,
          response: yao.is_response 
        }"
        :style="{ animationDelay: getAnimDelay(index) }"
      >
        <span class="yao-pos">{{ yao.position_name }}</span>
        
        <!-- 爻线绘制 -->
        <div class="yao-line-wrapper">
            <div v-if="yao.type === 'yang'" class="visual-line yang"></div>
            <div v-else class="visual-line yin">
                <span class="segment"></span>
                <span class="gap"></span>
                <span class="segment"></span>
            </div>
        </div>

        <span class="beast">{{ yao.beast }}</span>
        
        <div class="markers">
            <span v-if="yao.is_world" class="marker world">世</span>
            <span v-if="yao.is_response" class="marker response">应</span>
        </div>
        
        <span v-if="yao.changing" class="changing-mark">
            <span class="dot"></span>
        </span>
      </div>
    </div>
    
    <!-- 动爻说明 -->
    <div v-if="data.moving_positions.length > 0" class="moving-info">
      <span class="label">动爻：</span>
      <span class="positions">
        {{ data.moving_positions.map(p => ['初', '二', '三', '四', '五', '上'][p-1] + '爻').join('、') }}
      </span>
    </div>
    
    <!-- 卦辞解读区 -->
    <div v-if="data.interpretation?.original_hexagram" class="interpretation-section paper-texture">
      <div class="section-title">📜 卦辞解读</div>
      
      <div v-if="data.interpretation.original_hexagram.guaCi" class="gua-ci">
        <span class="quote">「{{ data.interpretation.original_hexagram.guaCi }}」</span>
      </div>
      
      <div v-if="data.interpretation.original_hexagram.guaCiExplain" class="gua-explain">
        {{ data.interpretation.original_hexagram.guaCiExplain }}
      </div>
      
      <div v-if="data.interpretation.original_hexagram.xiangCi" class="xiang-ci">
        <span class="label">《象》曰：</span>{{ data.interpretation.original_hexagram.xiangCi }}
      </div>
      
      <!-- 动爻爻辞 -->
      <div v-if="data.interpretation.moving_yaos?.length" class="moving-yaos">
        <div class="section-title">🔮 动爻爻辞</div>
        <div v-for="yao in data.interpretation.moving_yaos" :key="yao.position" class="yao-ci">
          <div class="yao-text">{{ yao.text }}</div>
          <div class="yao-explain">{{ yao.explain }}</div>
        </div>
      </div>
    </div>
    
    <!-- 基础解读摘要 -->
    <div v-if="data.interpretation?.interpretation_summary || data.interpretation_hint" class="interpretation-hint">
      <span class="hint-icon">💡</span>
      <span class="hint-text">
        {{ data.interpretation?.interpretation_summary || data.interpretation_hint }}
      </span>
    </div>
    
    <!-- AI 解卦区域 -->
    <div class="ai-section">
      <button 
        v-if="!aiContent && !isAILoading" 
        class="ai-btn" 
        @click="requestAIInterpretation"
      >
        <span class="sparkle">✨</span> 请求AI深入解卦
      </button>
      
      <div v-if="isAILoading" class="ai-loading">
        <div class="loading-spinner"></div>
        <span>AI正在推演天机...</span>
      </div>
      
      <div v-if="aiError" class="ai-error">
        {{ aiError }}
      </div>
      
      <div v-if="aiContent" class="ai-content paper-texture">
        <div class="section-title">🤖 AI解卦</div>
        <div class="ai-text" v-html="aiContent.replace(/\n/g, '<br>')"></div>
      </div>
    </div>
    
    <!-- 问题 -->
    <div v-if="data.question" class="question-display">
      <span class="label">所问：</span>
      <span class="question">{{ data.question }}</span>
    </div>
  </div>
</template>

<style scoped>
.liuyao-chart {
  width: 100%;
  max-width: 440px;
  margin-top: 16px;
  padding: 32px 24px;
  background: var(--bg-card);
  border: 1px solid var(--border-accent);
  border-radius: 4px;
  position: relative;
  overflow: hidden;
}

/* 纸质纹理效果 */
.paper-texture {
    position: relative;
    background: rgba(255, 255, 255, 0.02);
    box-shadow: inset 0 0 20px rgba(0,0,0,0.2);
}

.chart-header {
  text-align: center;
  margin-bottom: 28px;
  padding-bottom: 20px;
  border-bottom: 1px solid var(--border-subtle);
  position: relative;
}

.chart-header::after {
    content: '';
    position: absolute;
    bottom: -1px;
    left: 20%;
    width: 60%;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--accent-gold), transparent);
    opacity: 0.5;
}

.hexagram-display {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 24px;
}

.hexagram {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.symbol-box {
    width: 64px;
    height: 64px;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 1px solid var(--border-subtle);
    border-radius: 50%;
    background: radial-gradient(circle, rgba(212, 175, 55, 0.1) 0%, transparent 70%);
}

.symbol-text {
  font-size: 36px;
  line-height: 1;
  color: var(--accent-gold);
  filter: drop-shadow(0 0 5px rgba(212, 175, 55, 0.3));
}

.hexagram .name {
  font-size: 18px;
  font-weight: bold;
  font-family: 'SongTi', serif;
  color: var(--accent-gold);
  letter-spacing: 2px;
}

.hexagram.changed .name {
  color: var(--accent-jade);
}

.hexagram.changed .symbol-text {
    color: var(--accent-jade);
}

.hexagram.changed .symbol-box {
    background: radial-gradient(circle, rgba(0, 168, 150, 0.1) 0%, transparent 70%);
}

.arrow {
  font-size: 18px;
  color: var(--text-muted);
  opacity: 0.6;
}

/* 六爻行 */
.yaos-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 24px;
  padding: 0 10px;
}

.yao-row {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 6px 4px;
  position: relative;
  /* 初始不可见，由动画控制显示 */
  opacity: 0;
  animation: drawLine 0.6s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
}

@keyframes drawLine {
    from { opacity: 0; transform: translateY(10px) scaleX(0.9); }
    to { opacity: 1; transform: translateY(0) scaleX(1); }
}

.yao-pos {
  font-size: 12px;
  font-family: 'KaiTi', serif;
  color: var(--text-secondary);
  width: 32px;
  text-align: center;
}

/* 视觉化的爻线 */
.yao-line-wrapper {
    flex: 1;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0 10px;
}

.visual-line {
    height: 8px; /* 较粗的线条 */
    border-radius: 2px;
    width: 100%;
    background: var(--accent-gold);
    box-shadow: 0 1px 2px rgba(0,0,0,0.3);
    /* 模拟毛笔笔触不规则边缘 */
    filter: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='rough'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.05' numOctaves='2' result='noise'/%3E%3CfeDisplacementMap in='SourceGraphic' in2='noise' scale='2'/%3E%3C/filter%3E#rough");
    opacity: 0.9;
}

.visual-line.yin {
    background: transparent;
    display: flex;
    justify-content: space-between;
    box-shadow: none;
    filter: none; /* 阴爻分开容易出问题，简化处理 */
}

.visual-line.yin .segment {
    width: 42%;
    height: 100%;
    background: var(--accent-gold);
    border-radius: 2px;
    box-shadow: 0 1px 2px rgba(0,0,0,0.3);
    opacity: 0.9;
}

.yao-row.changing .visual-line, 
.yao-row.changing .visual-line.yin .segment {
    background: var(--accent-cinnabar);
    box-shadow: 0 0 8px rgba(217, 79, 69, 0.4);
}

.beast {
  font-size: 12px;
  font-family: 'KaiTi', serif;
  color: var(--accent-jade);
  width: 32px;
  text-align: right;
}

.markers {
    width: 20px;
    display: flex;
    justify-content: center;
}

.marker {
  font-size: 10px;
  padding: 1px 4px;
  border-radius: 2px;
  line-height: 1;
}

.marker.world {
  color: var(--accent-gold);
  border: 1px solid var(--accent-gold);
}

.marker.response {
  color: var(--accent-jade);
  border: 1px solid var(--accent-jade);
}

.changing-mark {
  position: absolute;
  right: -8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.changing-mark .dot {
    width: 6px;
    height: 6px;
    background: var(--accent-cinnabar);
    border-radius: 50%;
    box-shadow: 0 0 5px var(--accent-cinnabar);
    animation: pulse 1s infinite;
}

/* 动爻信息 */
.moving-info {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 20px;
  font-size: 14px;
  padding: 8px 16px;
  background: rgba(217, 79, 69, 0.1);
  border-radius: 4px;
  border-left: 2px solid var(--accent-cinnabar);
}

.moving-info .label {
  color: var(--text-secondary);
}

.moving-info .positions {
  color: var(--accent-cinnabar);
  font-weight: bold;
}

/* 解卦提示 */
.interpretation-hint {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px;
  background: rgba(212, 175, 55, 0.05);
  border: 1px solid rgba(212, 175, 55, 0.2);
  border-radius: 4px;
  margin-bottom: 20px;
}

.hint-icon {
  font-size: 18px;
}

.hint-text {
  font-size: 15px;
  color: var(--text-primary);
  line-height: 1.6;
}

/* 问题显示 */
.question-display {
  font-size: 14px;
  padding-top: 16px;
  border-top: 1px dashed var(--border-subtle);
  color: var(--text-muted);
}

.question-display .question {
  color: var(--text-secondary);
  font-style: italic;
}

/* 卦辞解读区 */
.interpretation-section {
  margin-bottom: 20px;
  padding: 20px;
  border-radius: 8px;
  border: 1px solid var(--border-subtle);
}

.section-title {
  font-size: 15px;
  font-weight: bold;
  color: var(--accent-gold);
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.gua-ci {
  margin-bottom: 16px;
  text-align: center;
}

.gua-ci .quote {
  font-size: 20px;
  font-family: 'SongTi', serif;
  color: var(--accent-gold);
  line-height: 1.5;
  text-shadow: 0 0 10px rgba(0,0,0,0.5);
}

.gua-explain {
  font-size: 15px;
  color: var(--text-primary);
  line-height: 1.8;
  margin-bottom: 16px;
  text-indent: 2em;
}

.xiang-ci {
  font-size: 14px;
  color: var(--text-secondary);
  padding: 12px;
  background: rgba(0,0,0,0.2);
  border-radius: 4px;
  margin-bottom: 16px;
  font-family: 'KaiTi', serif;
}

/* 动爻爻辞 */
.moving-yaos {
  margin-top: 24px;
  padding-top: 16px;
  border-top: 1px solid var(--border-subtle);
}

.yao-ci {
  margin-bottom: 16px;
  padding: 16px;
  background: rgba(217, 79, 69, 0.05);
  border-radius: 4px;
  border: 1px solid rgba(217, 79, 69, 0.2);
}

.yao-text {
  font-size: 16px;
  font-weight: bold;
  color: var(--accent-cinnabar);
  margin-bottom: 8px;
  font-family: 'SongTi', serif;
}

.yao-explain {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.6;
}

/* AI 解卦区 */
.ai-section {
  margin: 24px 0;
}

.ai-btn {
  width: 100%;
  padding: 14px 24px;
  background: linear-gradient(135deg, rgba(212, 175, 55, 0.1) 0%, rgba(0, 168, 150, 0.1) 100%);
  border: 1px solid var(--border-accent);
  border-radius: 4px;
  color: var(--accent-gold);
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.ai-btn:hover {
  background: linear-gradient(135deg, rgba(212, 175, 55, 0.2) 0%, rgba(0, 168, 150, 0.2) 100%);
  border-color: var(--accent-gold);
  box-shadow: 0 0 20px rgba(212, 175, 55, 0.15);
}

.ai-btn .sparkle {
    display: inline-block;
    animation: pulse 1s infinite;
}

.ai-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 24px;
  color: var(--text-secondary);
  font-family: 'KaiTi', serif;
}

.loading-spinner {
  width: 24px;
  height: 24px;
  border: 2px solid var(--border-subtle);
  border-top-color: var(--accent-gold);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.ai-error {
  padding: 16px;
  background: rgba(217, 79, 69, 0.1);
  border: 1px solid rgba(217, 79, 69, 0.3);
  border-radius: 4px;
  color: var(--accent-cinnabar);
  text-align: center;
  font-size: 14px;
}

.ai-content {
  padding: 24px;
  border: 1px solid var(--accent-jade);
  border-radius: 8px;
  position: relative;
}

.ai-content::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 4px;
    background: linear-gradient(90deg, var(--accent-jade), transparent);
}

.ai-text {
  font-size: 15px;
  color: var(--text-primary);
  line-height: 1.8;
  text-align: justify;
}
</style>
