<script setup lang="ts">
import { ref, computed } from 'vue';
import { gsap } from 'gsap';

const emit = defineEmits<{
  complete: [results: number[]]
}>();

const currentToss = ref(0);
const results = ref<number[]>([]);
const coins = ref<{ id: number; side: 'front' | 'back'; rotating: boolean }[]>([
  { id: 1, side: 'front', rotating: false },
  { id: 2, side: 'front', rotating: false },
  { id: 3, side: 'front', rotating: false }
]);
const isAnimating = ref(false);
const showResult = ref(false);
const currentResult = ref<{ value: number; name: string } | null>(null);

const tossLabels = ['初爻', '二爻', '三爻', '四爻', '五爻', '上爻'];
const resultNames = {
  6: { name: '老阴', symbol: '⚋', changing: true },
  7: { name: '少阳', symbol: '⚊', changing: false },
  8: { name: '少阴', symbol: '⚋', changing: false },
  9: { name: '老阳', symbol: '⚊', changing: true }
};

const progress = computed(() => `${currentToss.value}/6`);
const canToss = computed(() => currentToss.value < 6 && !isAnimating.value);
const isComplete = computed(() => currentToss.value === 6);

// 模拟抛币
function simulateToss(): number {
  // 三枚铜钱: 正面=3, 反面=2
  const coinResults = Array.from({ length: 3 }, () => Math.random() > 0.5 ? 3 : 2);
  return coinResults.reduce((a, b) => a + b, 0);
}

// 抛币动画
async function tossCoin() {
  if (!canToss.value) return;
  
  isAnimating.value = true;
  showResult.value = false;
  
  // 动画: 三枚铜钱旋转
  const coinElements = document.querySelectorAll('.coin');
  
  // 随机每个铜钱的最终状态
  const finalSides: ('front' | 'back')[] = [];
  coins.value.forEach((coin, i) => {
    coin.rotating = true;
    const isFront = Math.random() > 0.5;
    finalSides.push(isFront ? 'front' : 'back');
    
    // 旋转动画
    gsap.to(coinElements[i], {
      rotateY: 720 + (isFront ? 0 : 180),
      duration: 1.2 + i * 0.2,
      ease: 'power2.out',
      onComplete: () => {
        coin.side = finalSides[i];
        coin.rotating = false;
      }
    });
  });
  
  // 等待动画完成
  await new Promise(resolve => setTimeout(resolve, 1800));
  
  // 计算结果
  const result = simulateToss();
  results.value.push(result);
  currentResult.value = {
    value: result,
    name: resultNames[result as keyof typeof resultNames]?.name || ''
  };
  showResult.value = true;
  
  currentToss.value++;
  isAnimating.value = false;
  
  // 检查是否完成
  if (currentToss.value === 6) {
    setTimeout(() => {
      emit('complete', [...results.value]);
    }, 1000);
  }
}

// 重置
function reset() {
  currentToss.value = 0;
  results.value = [];
  showResult.value = false;
  currentResult.value = null;
  coins.value.forEach(c => {
    c.side = 'front';
    c.rotating = false;
  });
}
</script>

<template>
  <div class="coin-toss-widget card">
    <div class="toss-header">
      <span class="title">🪙 金钱卦</span>
      <span class="progress">{{ progress }}</span>
    </div>
    
    <div class="current-yao" v-if="!isComplete">
      正在起：<strong>{{ tossLabels[currentToss] }}</strong>
    </div>
    
    <!-- 铜钱容器 -->
    <div class="coins-container">
      <div 
        v-for="coin in coins" 
        :key="coin.id"
        class="coin"
        :class="{ rotating: coin.rotating, [coin.side]: true }"
      >
        <div class="coin-front">
          <span>乾</span>
        </div>
        <div class="coin-back">
          <span>隆</span>
        </div>
      </div>
    </div>
    
    <!-- 当前结果 -->
    <Transition name="fade">
      <div v-if="showResult && currentResult" class="toss-result">
        <span class="result-symbol">{{ resultNames[currentResult.value as keyof typeof resultNames]?.symbol }}</span>
        <span class="result-name">{{ currentResult.name }}</span>
        <span v-if="resultNames[currentResult.value as keyof typeof resultNames]?.changing" class="changing-tag">变爻</span>
      </div>
    </Transition>
    
    <!-- 已抛结果列表 -->
    <div class="results-list" v-if="results.length > 0">
      <div 
        v-for="(r, i) in results" 
        :key="i"
        class="result-item"
        :class="{ changing: resultNames[r as keyof typeof resultNames]?.changing }"
      >
        <span class="yao-label">{{ tossLabels[i] }}</span>
        <span class="yao-symbol">{{ resultNames[r as keyof typeof resultNames]?.symbol }}</span>
      </div>
    </div>
    
    <!-- 操作按钮 -->
    <div class="actions">
      <button 
        v-if="!isComplete"
        class="btn btn-primary toss-btn"
        :disabled="!canToss"
        @click="tossCoin"
      >
        {{ isAnimating ? '起卦中...' : '摇一摇' }}
      </button>
      <div v-else class="complete-message">
        ✨ 六爻已成
      </div>
    </div>
  </div>
</template>

<style scoped>
.coin-toss-widget {
  width: 100%;
  max-width: 360px;
  margin-top: 12px;
  text-align: center;
}

.toss-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--border-subtle);
}

.title {
  font-size: 18px;
  color: var(--accent-gold);
  letter-spacing: 2px;
}

.progress {
  font-size: 14px;
  color: var(--text-secondary);
}

.current-yao {
  font-size: 14px;
  color: var(--text-secondary);
  margin-bottom: 20px;
}

.current-yao strong {
  color: var(--accent-jade);
}

/* 铜钱样式 */
.coins-container {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin: 24px 0;
  perspective: 1000px;
}

.coin {
  width: 70px;
  height: 70px;
  position: relative;
  transform-style: preserve-3d;
  transition: transform 0.1s;
}

.coin-front, .coin-back {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-weight: bold;
  backface-visibility: hidden;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}

.coin-front {
  background: linear-gradient(135deg, #d4af37, #f0d878, #d4af37);
  color: #5c4a1f;
  border: 3px solid #c9a227;
}

.coin-back {
  background: linear-gradient(135deg, #8b7355, #a08060, #8b7355);
  color: #4a3f2f;
  border: 3px solid #6b5b45;
  transform: rotateY(180deg);
}

.coin.rotating {
  animation: none;
}

/* 结果显示 */
.toss-result {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin: 16px 0;
  padding: 12px;
  background: var(--bg-tertiary);
  border-radius: 8px;
}

.result-symbol {
  font-size: 28px;
  color: var(--accent-gold);
}

.result-name {
  font-size: 16px;
  color: var(--text-primary);
}

.changing-tag {
  font-size: 12px;
  padding: 2px 8px;
  background: rgba(217, 79, 69, 0.2);
  color: #d94f45;
  border-radius: 4px;
}

/* 结果列表 */
.results-list {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin: 16px 0;
  flex-wrap: wrap;
}

.result-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 8px 12px;
  background: var(--bg-tertiary);
  border-radius: 8px;
  min-width: 50px;
}

.result-item.changing {
  border: 1px solid rgba(217, 79, 69, 0.5);
}

.yao-label {
  font-size: 10px;
  color: var(--text-muted);
}

.yao-symbol {
  font-size: 18px;
  color: var(--accent-gold);
}

/* 按钮 */
.actions {
  margin-top: 20px;
}

.toss-btn {
  width: 100%;
  padding: 14px;
  font-size: 18px;
  letter-spacing: 4px;
}

.toss-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.complete-message {
  font-size: 18px;
  color: var(--accent-jade);
  letter-spacing: 2px;
}

/* 动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@keyframes coinFlip {
  0% { transform: rotateY(0deg); }
  100% { transform: rotateY(720deg); }
}
</style>
