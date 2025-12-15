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

function getYaoStyle(yao: Yao) {
  if (yao.changing) {
    return { color: '#d94f45' };
  }
  return { color: 'var(--accent-gold)' };
}

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
</script>

<template>
  <div class="liuyao-chart card-glow">
    <!-- 卦象头部 -->
    <div class="chart-header">
      <div class="hexagram-display">
        <div class="hexagram original">
          <span class="symbol">{{ data.original_hexagram.upper_symbol }}{{ data.original_hexagram.lower_symbol }}</span>
          <span class="name">{{ data.original_hexagram.name }}</span>
        </div>
        <span v-if="data.changed_hexagram" class="arrow">→</span>
        <div v-if="data.changed_hexagram" class="hexagram changed">
          <span class="symbol">{{ data.changed_hexagram.upper_symbol }}{{ data.changed_hexagram.lower_symbol }}</span>
          <span class="name">{{ data.changed_hexagram.name }}</span>
        </div>
      </div>
    </div>
    
    <!-- 六爻列表 -->
    <div class="yaos-container">
      <div 
        v-for="yao in [...data.yaos].reverse()" 
        :key="yao.position"
        class="yao-row"
        :class="{ 
          changing: yao.changing,
          world: yao.is_world,
          response: yao.is_response 
        }"
      >
        <span class="yao-pos">{{ yao.position_name }}</span>
        <span class="yao-line" :style="getYaoStyle(yao)">
          {{ yao.type === 'yang' ? '━━━━━' : '━━ ━━' }}
        </span>
        <span class="beast">{{ yao.beast }}</span>
        <span v-if="yao.is_world" class="marker world">世</span>
        <span v-if="yao.is_response" class="marker response">应</span>
        <span v-if="yao.changing" class="changing-mark">○</span>
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
    <div v-if="data.interpretation?.original_hexagram" class="interpretation-section">
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
    <div v-if="data.interpretation?.interpretation_summary" class="interpretation-hint">
      <span class="hint-icon">💡</span>
      <span class="hint-text">{{ data.interpretation.interpretation_summary }}</span>
    </div>
    <div v-else class="interpretation-hint">
      <span class="hint-icon">💡</span>
      <span class="hint-text">{{ data.interpretation_hint }}</span>
    </div>
    
    <!-- AI 解卦区域 -->
    <div class="ai-section">
      <button 
        v-if="!aiContent && !isAILoading" 
        class="ai-btn" 
        @click="requestAIInterpretation"
      >
        ✨ 请求AI解卦
      </button>
      
      <div v-if="isAILoading" class="ai-loading">
        <div class="loading-spinner"></div>
        <span>AI正在解读卦象...</span>
      </div>
      
      <div v-if="aiError" class="ai-error">
        {{ aiError }}
      </div>
      
      <div v-if="aiContent" class="ai-content">
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
  max-width: 400px;
  margin-top: 12px;
  padding: 24px;
  background: var(--bg-card);
  border: 1px solid var(--border-accent);
  border-radius: 16px;
}

.chart-header {
  text-align: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--border-subtle);
}

.hexagram-display {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
}

.hexagram {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.hexagram .symbol {
  font-size: 32px;
  line-height: 1;
}

.hexagram .name {
  font-size: 16px;
  color: var(--accent-gold);
}

.hexagram.changed .name {
  color: var(--accent-jade);
}

.arrow {
  font-size: 24px;
  color: var(--text-secondary);
}

/* 六爻行 */
.yaos-container {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 20px;
}

.yao-row {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 12px;
  background: var(--bg-tertiary);
  border-radius: 8px;
  position: relative;
}

.yao-row.changing {
  border: 1px solid rgba(217, 79, 69, 0.4);
}

.yao-pos {
  font-size: 12px;
  color: var(--text-secondary);
  width: 40px;
}

.yao-line {
  font-size: 20px;
  font-family: monospace;
  letter-spacing: 2px;
  flex: 1;
  text-align: center;
}

.beast {
  font-size: 12px;
  color: var(--accent-jade);
  width: 40px;
  text-align: right;
}

.marker {
  font-size: 12px;
  padding: 2px 6px;
  border-radius: 4px;
}

.marker.world {
  background: rgba(212, 175, 55, 0.2);
  color: var(--accent-gold);
}

.marker.response {
  background: rgba(0, 168, 150, 0.2);
  color: var(--accent-jade);
}

.changing-mark {
  position: absolute;
  right: 8px;
  color: #d94f45;
  font-size: 14px;
}

/* 动爻信息 */
.moving-info {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  font-size: 14px;
}

.moving-info .label {
  color: var(--text-secondary);
}

.moving-info .positions {
  color: #d94f45;
}

/* 解卦提示 */
.interpretation-hint {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  padding: 12px;
  background: rgba(212, 175, 55, 0.1);
  border-radius: 8px;
  margin-bottom: 12px;
}

.hint-icon {
  font-size: 16px;
}

.hint-text {
  font-size: 14px;
  color: var(--text-primary);
  line-height: 1.5;
}

/* 问题显示 */
.question-display {
  font-size: 14px;
  padding-top: 12px;
  border-top: 1px solid var(--border-subtle);
}

.question-display .label {
  color: var(--text-secondary);
}

.question-display .question {
  color: var(--text-primary);
}

/* 卦辞解读区 */
.interpretation-section {
  margin-bottom: 16px;
  padding: 16px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 12px;
  border: 1px solid var(--border-subtle);
}

.section-title {
  font-size: 14px;
  color: var(--accent-gold);
  margin-bottom: 12px;
  letter-spacing: 1px;
}

.gua-ci {
  margin-bottom: 12px;
}

.gua-ci .quote {
  font-size: 16px;
  color: var(--accent-gold);
  font-style: italic;
  line-height: 1.6;
}

.gua-explain {
  font-size: 14px;
  color: var(--text-primary);
  line-height: 1.7;
  margin-bottom: 12px;
}

.xiang-ci {
  font-size: 14px;
  color: var(--text-secondary);
  padding: 8px 12px;
  background: rgba(212, 175, 55, 0.1);
  border-radius: 6px;
  margin-bottom: 12px;
}

.xiang-ci .label {
  color: var(--accent-gold);
}

/* 动爻爻辞 */
.moving-yaos {
  margin-top: 16px;
  padding-top: 12px;
  border-top: 1px dashed var(--border-subtle);
}

.yao-ci {
  margin-bottom: 12px;
  padding: 10px;
  background: rgba(217, 79, 69, 0.1);
  border-radius: 8px;
  border-left: 3px solid #d94f45;
}

.yao-text {
  font-size: 14px;
  color: #d94f45;
  margin-bottom: 6px;
}

.yao-explain {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.5;
}

/* AI 解卦区 */
.ai-section {
  margin: 16px 0;
}

.ai-btn {
  width: 100%;
  padding: 12px 24px;
  background: linear-gradient(135deg, rgba(212, 175, 55, 0.2) 0%, rgba(0, 168, 150, 0.2) 100%);
  border: 1px solid var(--accent-gold);
  border-radius: 24px;
  color: var(--accent-gold);
  font-size: 15px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.ai-btn:hover {
  background: linear-gradient(135deg, rgba(212, 175, 55, 0.3) 0%, rgba(0, 168, 150, 0.3) 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3);
}

.ai-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 20px;
  color: var(--text-secondary);
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid var(--border-subtle);
  border-top-color: var(--accent-gold);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.ai-error {
  padding: 12px;
  background: rgba(217, 79, 69, 0.1);
  border: 1px solid rgba(217, 79, 69, 0.3);
  border-radius: 8px;
  color: #d94f45;
  text-align: center;
  font-size: 14px;
}

.ai-content {
  padding: 16px;
  background: linear-gradient(135deg, rgba(0, 168, 150, 0.05) 0%, rgba(212, 175, 55, 0.05) 100%);
  border: 1px solid var(--accent-jade);
  border-radius: 12px;
}

.ai-text {
  font-size: 14px;
  color: var(--text-primary);
  line-height: 1.8;
}
</style>
