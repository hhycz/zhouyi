<script setup lang="ts">
import { ref, computed } from 'vue';
import { gsap } from 'gsap';

const emit = defineEmits<{
  complete: [results: number[]]
}>();

const currentToss = ref(0);
const results = ref<number[]>([]);
const coins = ref<{ id: number; side: 'front' | 'back'; x: number; y: number; rotation: number }[]>([
  { id: 1, side: 'front', x: 0, y: 0, rotation: 0 },
  { id: 2, side: 'front', x: 0, y: 0, rotation: 0 },
  { id: 3, side: 'front', x: 0, y: 0, rotation: 0 }
]);
const isShaking = ref(false);
const isTossing = ref(false);
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
const canInteract = computed(() => currentToss.value < 6 && !isTossing.value);
const isComplete = computed(() => currentToss.value === 6);

// 模拟抛币
function simulateToss(): number {
  // 三枚铜钱: 正面(3)+反面(2)
  const coinResults = Array.from({ length: 3 }, () => Math.random() > 0.5 ? 3 : 2);
  return coinResults.reduce((a, b) => a + b, 0);
}

// 开始摇卦
function startShake() {
  if (!canInteract.value || isShaking.value) return;
  isShaking.value = true;
  showResult.value = false;

  // 简单的震动动画
  const coinElements = document.querySelectorAll('.coin');
  gsap.to(coinElements, {
    x: 'random(-5, 5)',
    y: 'random(-5, 5)',
    duration: 0.1,
    repeat: -1,
    yoyo: true,
    ease: 'power1.inOut'
  });
}

// 停止摇卦并抛出
async function tossCoin() {
  if (!isShaking.value) return;
  
  isShaking.value = false;
  isTossing.value = true;
  
  // 停止震动，开始抛掷动画
  gsap.killTweensOf('.coin');
  
  const coinElements = document.querySelectorAll('.coin');
  
  // 随机每个铜钱的最终状态
  const finalSides: ('front' | 'back')[] = [];
  
  // 抛掷动画
  const tl = gsap.timeline();
  
  coins.value.forEach((coin, i) => {
    const isFront = Math.random() > 0.5;
    finalSides.push(isFront ? 'front' : 'back');
    
    // 随机落地位置散开
    const targetX = (Math.random() - 0.5) * 60; // +/- 30px
    const targetY = (Math.random() - 0.5) * 60; // +/- 30px
    const extraRot = Math.random() * 360;

    tl.to(coinElements[i], {
      y: -150, // 抛高
      scale: 1.5,
      rotateY: "+=1080", // 旋转多圈
      rotateZ: Math.random() * 180,
      duration: 0.6,
      ease: 'power2.out'
    }, 0);

    tl.to(coinElements[i], {
      y: targetY, // 落地
      x: targetX,
      scale: 1,
      rotateY: `+=${720 + (isFront ? 0 : 180)}`, // 确保落地面正确
      rotateZ: extraRot,
      duration: 0.8,
      ease: 'bounce.out',
      onComplete: () => {
        coin.side = finalSides[i];
      }
    }, 0.6);
  });
  
  await tl;
  
  // 计算结果
  const result = simulateToss();
  results.value.push(result);
  currentResult.value = {
    value: result,
    name: resultNames[result as keyof typeof resultNames]?.name || ''
  };
  
  // 短暂延迟显示结果
  setTimeout(() => {
    showResult.value = true;
    currentToss.value++;
    isTossing.value = false;
    
    // 归位动画 (准备下一次)
    if (currentToss.value < 6) {
        gsap.to(coinElements, {
            x: 0,
            y: 0,
            rotateZ: 0,
            delay: 1.5, // 让用户看一会
            duration: 0.5,
            ease: 'power2.inOut',
            onComplete: () => {
                showResult.value = false;
            }
        });
    } else {
        // 完成
        setTimeout(() => {
          emit('complete', [...results.value]);
        }, 1500);
    }
  }, 500);
}
</script>

<template>
  <div class="coin-toss-widget card">
    <div class="toss-header">
      <span class="title">🪙 六爻金钱卦</span>
      <span class="progress">{{ progress }}</span>
    </div>
    
    <div class="current-yao" v-if="!isComplete">
      <span class="hint">诚心默念，摇卦六次</span>
      <div class="yao-highlight">正在起：<strong>{{ tossLabels[currentToss] }}</strong></div>
    </div>
    
    <!-- 铜钱容器 -->
    <div class="coins-container" :class="{ 'shaking': isShaking }">
      <div 
        v-for="coin in coins" 
        :key="coin.id"
        class="coin"
        :class="[coin.side]"
      >
        <div class="coin-face coin-front">
          <div class="coin-inner">
             <span class="text top">乾隆</span>
             <span class="text bottom">通宝</span>
          </div>
        </div>
        <div class="coin-face coin-back">
          <div class="coin-inner pattern"></div>
        </div>
      </div>
    </div>
    
    <!-- 操作提示/状态 -->
    <div class="status-text">
        <span v-if="isShaking">点击停止抛出...</span>
        <span v-else-if="isTossing">...</span>
        <span v-else-if="showResult && currentResult" class="result-text">
            {{ resultNames[currentResult.value as keyof typeof resultNames]?.symbol }} 
            {{ currentResult.name }}
            <span v-if="resultNames[currentResult.value as keyof typeof resultNames]?.changing" class="changing-tag">动</span>
        </span>
        <span v-else>点击开始摇卦</span>
    </div>
    
    <!-- 已抛结果列表 -->
    <div class="results-list" v-if="results.length > 0">
      <div 
        v-for="(r, i) in results" 
        :key="i"
        class="result-item"
        :class="{ changing: resultNames[r as keyof typeof resultNames]?.changing, active: i === currentToss - 1 }"
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
        :class="{ 'is-shaking': isShaking }"
        :disabled="isTossing"
        @mousedown="startShake"
        @mouseup="tossCoin"
        @touchstart.prevent="startShake"
        @touchend.prevent="tossCoin"
      >
        {{ isShaking ? '抛出' : (isTossing ? '占算中...' : '按住摇卦') }}
      </button>
      <div v-else class="complete-message">
        ✨ 卦象已成 ✨
      </div>
    </div>
  </div>
</template>

<style scoped>
.coin-toss-widget {
  width: 100%;
  max-width: 380px;
  margin-top: 12px;
  text-align: center;
  background: var(--bg-card);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-accent);
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
  font-family: 'SongTi', serif;
  color: var(--accent-gold);
}

.progress {
  font-size: 14px;
  color: var(--text-secondary);
  font-feature-settings: "tnum";
}

.current-yao {
  margin-bottom: 24px;
}

.hint {
  font-size: 12px;
  color: var(--text-muted);
  display: block;
  margin-bottom: 4px;
}

.yao-highlight {
  font-size: 15px;
  color: var(--text-primary);
}

.yao-highlight strong {
  color: var(--accent-gold);
  font-size: 18px;
}

/* 铜钱容器 */
.coins-container {
  height: 180px;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 15px;
  position: relative;
  perspective: 1000px;
}

.coin {
  width: 80px;
  height: 80px;
  position: relative;
  transform-style: preserve-3d;
  will-change: transform;
}

.coin-face {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  backface-visibility: hidden;
  box-shadow: 
    inset 0 0 10px rgba(0,0,0,0.5),
    0 4px 8px rgba(0,0,0,0.3);
  display: flex;
  align-items: center;
  justify-content: center;
}

.coin-front {
  background: radial-gradient(circle at 30% 30%, #f0d878, #d4af37, #8a7024);
  color: #5c4a1f;
  border: 4px solid #b89628;
}

.coin-front::before {
    content: '';
    position: absolute;
    width: 24px;
    height: 24px;
    background: #000;
    opacity: 0.3;
}

.coin-inner {
    width: 65%;
    height: 65%;
    border: 1px solid rgba(0,0,0,0.2);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
}

.coin-front .text {
    font-family: "KaiTi", serif;
    font-weight: bold;
    font-size: 14px;
    line-height: 1;
}

.coin-front .text.top { margin-bottom: 24px; }
.coin-front .text.bottom { margin-top: 24px; }

.coin-back {
  background: radial-gradient(circle at 30% 30%, #a08060, #8b7355, #4a3f2f);
  color: #4a3f2f;
  transform: rotateY(180deg);
  border: 4px solid #6b5b45;
}

.pattern {
    border: 2px dashed rgba(0,0,0,0.2);
    width: 60%;
    height: 60%;
}

/* 状态文本 */
.status-text {
    height: 30px;
    margin: 10px 0;
    font-size: 16px;
    color: var(--accent-gold-light);
    display: flex;
    align-items: center;
    justify-content: center;
}

.result-text {
    font-size: 20px;
    font-weight: bold;
    display: flex;
    align-items: center;
    gap: 8px;
}

.changing-tag {
    font-size: 10px;
    background: var(--accent-cinnabar);
    color: #fff;
    padding: 2px 6px;
    border-radius: 4px;
    transform: translateY(-2px);
}

/* 结果列表 */
.results-list {
  display: flex;
  justify-content: center;
  gap: 6px;
  margin: 16px 0;
  padding: 10px;
  background: rgba(0,0,0,0.2);
  border-radius: 8px;
}

.result-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 6px 4px;
  border-radius: 4px;
  min-width: 40px;
  transition: all 0.3s;
  opacity: 0.6;
}

.result-item.active {
    opacity: 1;
    background: rgba(212, 175, 55, 0.1);
    box-shadow: 0 0 10px rgba(212, 175, 55, 0.1);
}

.result-item.changing .yao-symbol {
  color: var(--accent-cinnabar);
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
  height: 56px;
  font-size: 18px;
  letter-spacing: 4px;
  background: linear-gradient(135deg, var(--bg-tertiary), var(--bg-secondary));
  border: 1px solid var(--accent-gold);
  color: var(--accent-gold);
  transition: all 0.2s;
}

.toss-btn:active, .toss-btn.is-shaking {
    background: var(--accent-gold);
    color: var(--bg-primary);
    transform: scale(0.98);
}

.toss-btn:disabled {
  opacity: 0.7;
  cursor: wait;
}

.complete-message {
  font-size: 20px;
  color: var(--accent-gold);
  letter-spacing: 4px;
  animation: pulse 2s infinite;
}
</style>
