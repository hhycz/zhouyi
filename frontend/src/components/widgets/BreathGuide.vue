<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';

const emit = defineEmits<{
  complete: []
}>();

const phase = ref<'inhale' | 'hold' | 'exhale'>('inhale');
const currentBreath = ref(1);
const totalBreaths = 3;
const isActive = ref(true);

const phaseLabels = {
  inhale: '吸气',
  hold: '屏息',
  exhale: '呼气'
};

let animationTimer: number | null = null;

function startBreathing() {
  const cycle = () => {
    if (!isActive.value) return;
    
    // 吸气 4秒
    phase.value = 'inhale';
    animationTimer = window.setTimeout(() => {
      if (!isActive.value) return;
      
      // 屏息 2秒
      phase.value = 'hold';
      animationTimer = window.setTimeout(() => {
        if (!isActive.value) return;
        
        // 呼气 4秒
        phase.value = 'exhale';
        animationTimer = window.setTimeout(() => {
          if (!isActive.value) return;
          
          if (currentBreath.value < totalBreaths) {
            currentBreath.value++;
            cycle();
          } else {
            // 完成
            emit('complete');
          }
        }, 4000);
      }, 2000);
    }, 4000);
  };
  
  cycle();
}

function skip() {
  isActive.value = false;
  if (animationTimer) {
    clearTimeout(animationTimer);
  }
  emit('complete');
}

onMounted(() => {
  startBreathing();
});

onUnmounted(() => {
  isActive.value = false;
  if (animationTimer) {
    clearTimeout(animationTimer);
  }
});
</script>

<template>
  <div class="breath-guide">
    <div class="breath-container">
      <!-- 呼吸圆环 -->
      <div 
        class="breath-circle"
        :class="phase"
      >
        <div class="inner-glow"></div>
        <span class="phase-text">{{ phaseLabels[phase] }}</span>
      </div>
      
      <!-- 提示文字 -->
      <p class="instruction">静心凝神，心诚则灵</p>
      
      <!-- 进度指示 -->
      <div class="progress">
        <span 
          v-for="i in totalBreaths" 
          :key="i"
          class="dot"
          :class="{ active: i <= currentBreath, current: i === currentBreath }"
        ></span>
      </div>
      
      <!-- 跳过按钮 -->
      <button class="skip-btn" @click="skip">跳过</button>
    </div>
  </div>
</template>

<style scoped>
.breath-guide {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px 20px;
  animation: fadeIn 0.5s ease-out;
}

.breath-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 24px;
}

/* 呼吸圆环 */
.breath-circle {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  background: radial-gradient(circle, rgba(212, 175, 55, 0.1) 0%, transparent 70%);
  border: 2px solid var(--accent-gold);
  transition: transform 4s ease-in-out, box-shadow 4s ease-in-out;
}

.breath-circle.inhale {
  transform: scale(1.3);
  box-shadow: 
    0 0 40px rgba(212, 175, 55, 0.4),
    0 0 80px rgba(212, 175, 55, 0.2),
    inset 0 0 30px rgba(212, 175, 55, 0.1);
}

.breath-circle.hold {
  transform: scale(1.3);
  box-shadow: 
    0 0 50px rgba(212, 175, 55, 0.5),
    0 0 100px rgba(212, 175, 55, 0.3),
    inset 0 0 40px rgba(212, 175, 55, 0.15);
  transition: transform 0.3s, box-shadow 2s ease-in-out;
}

.breath-circle.exhale {
  transform: scale(1);
  box-shadow: 
    0 0 20px rgba(212, 175, 55, 0.2),
    0 0 40px rgba(212, 175, 55, 0.1);
}

.inner-glow {
  position: absolute;
  width: 60%;
  height: 60%;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(212, 175, 55, 0.3) 0%, transparent 70%);
  animation: pulse 2s ease-in-out infinite;
}

.phase-text {
  font-size: 20px;
  color: var(--accent-gold);
  letter-spacing: 4px;
  z-index: 1;
  text-shadow: 0 0 10px rgba(212, 175, 55, 0.5);
}

.instruction {
  font-size: 16px;
  color: var(--text-secondary);
  letter-spacing: 2px;
  text-align: center;
  margin: 0;
}

/* 进度点 */
.progress {
  display: flex;
  gap: 12px;
}

.dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--border-subtle);
  transition: all 0.3s ease;
}

.dot.active {
  background: var(--accent-gold);
}

.dot.current {
  box-shadow: 0 0 10px var(--accent-gold);
  animation: glow 1s ease-in-out infinite;
}

/* 跳过按钮 */
.skip-btn {
  margin-top: 20px;
  padding: 8px 24px;
  background: transparent;
  border: 1px solid var(--border-subtle);
  color: var(--text-secondary);
  border-radius: 20px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s ease;
}

.skip-btn:hover {
  border-color: var(--accent-gold);
  color: var(--accent-gold);
}

@keyframes pulse {
  0%, 100% { opacity: 0.5; transform: scale(0.9); }
  50% { opacity: 1; transform: scale(1.1); }
}

@keyframes glow {
  0%, 100% { box-shadow: 0 0 5px var(--accent-gold); }
  50% { box-shadow: 0 0 15px var(--accent-gold); }
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
