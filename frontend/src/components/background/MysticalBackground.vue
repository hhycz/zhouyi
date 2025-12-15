<script setup lang="ts">
/**
 * 周易神秘背景组件
 * 包含八卦图、阴阳鱼、星辰粒子等装饰元素
 */
import { ref, onMounted, onUnmounted } from 'vue';

const baguaRotation = ref(0);
let animationId: number | null = null;

// 缓慢旋转八卦图
function animate() {
  baguaRotation.value += 0.02;
  animationId = requestAnimationFrame(animate);
}

onMounted(() => {
  animate();
});

onUnmounted(() => {
  if (animationId) {
    cancelAnimationFrame(animationId);
  }
});
</script>

<template>
  <div class="mystical-background">
    <!-- 星辰粒子层 -->
    <div class="stars-layer">
      <div v-for="i in 50" :key="i" class="star" :style="{
        left: `${Math.random() * 100}%`,
        top: `${Math.random() * 100}%`,
        animationDelay: `${Math.random() * 3}s`,
        animationDuration: `${2 + Math.random() * 3}s`
      }"></div>
    </div>
    
    <!-- 八卦阵背景 -->
    <div class="bagua-layer">
      <div class="bagua-container" :style="{ transform: `rotate(${baguaRotation}deg)` }">
        <!-- 外圈八卦符号 -->
        <div class="bagua-symbols">
          <span class="trigram" style="--angle: 0deg">☰</span>
          <span class="trigram" style="--angle: 45deg">☱</span>
          <span class="trigram" style="--angle: 90deg">☲</span>
          <span class="trigram" style="--angle: 135deg">☳</span>
          <span class="trigram" style="--angle: 180deg">☴</span>
          <span class="trigram" style="--angle: 225deg">☵</span>
          <span class="trigram" style="--angle: 270deg">☶</span>
          <span class="trigram" style="--angle: 315deg">☷</span>
        </div>
        
        <!-- 太极阴阳鱼 -->
        <div class="taiji">
          <div class="taiji-half yang">
            <div class="eye"></div>
          </div>
          <div class="taiji-half yin">
            <div class="eye"></div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 水墨晕染层 -->
    <div class="ink-wash-layer">
      <div class="ink-blob blob1"></div>
      <div class="ink-blob blob2"></div>
      <div class="ink-blob blob3"></div>
    </div>
    
    <!-- 金色光晕圈 -->
    <div class="aura-rings">
      <div class="ring ring1"></div>
      <div class="ring ring2"></div>
      <div class="ring ring3"></div>
    </div>
    
    <!-- 顶部装饰图案 -->
    <div class="top-ornament">
      <div class="ornament-line"></div>
      <span class="ornament-symbol">☯</span>
      <div class="ornament-line"></div>
    </div>
    
    <!-- 底部装饰 -->
    <div class="bottom-ornament">
      <span class="hexagram-symbol">䷀</span>
      <span class="hexagram-symbol">䷁</span>
      <span class="hexagram-symbol">䷂</span>
    </div>
  </div>
</template>

<style scoped>
.mystical-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  overflow: hidden;
  z-index: 0;
}

/* 星辰粒子 */
.stars-layer {
  position: absolute;
  width: 100%;
  height: 100%;
}

.star {
  position: absolute;
  width: 2px;
  height: 2px;
  background: rgba(212, 175, 55, 0.6);
  border-radius: 50%;
  animation: twinkle 3s ease-in-out infinite;
}

@keyframes twinkle {
  0%, 100% { opacity: 0.2; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.5); }
}

/* 八卦阵 */
.bagua-layer {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.bagua-container {
  position: relative;
  width: 400px;
  height: 400px;
  opacity: 0.08;
}

.bagua-symbols {
  position: absolute;
  width: 100%;
  height: 100%;
}

.trigram {
  position: absolute;
  font-size: 32px;
  color: var(--accent-gold);
  top: 50%;
  left: 50%;
  transform: rotate(var(--angle)) translateY(-180px) rotate(calc(-1 * var(--angle)));
  text-shadow: 0 0 10px rgba(212, 175, 55, 0.5);
}

/* 太极阴阳 */
.taiji {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 120px;
  height: 120px;
  border-radius: 50%;
  overflow: hidden;
  box-shadow: 0 0 40px rgba(212, 175, 55, 0.3);
}

.taiji-half {
  position: absolute;
  width: 100%;
  height: 50%;
}

.taiji-half.yang {
  top: 0;
  background: radial-gradient(circle at 50% 100%, #e8e6e3 0%, #e8e6e3 25%, transparent 25%),
              radial-gradient(circle at 50% 0%, transparent 0%, transparent 25%, #e8e6e3 25%);
  background-size: 60px 60px, 60px 60px;
  background-position: 0 0, 60px 0;
  background-color: #e8e6e3;
  border-radius: 60px 60px 0 0;
}

.taiji-half.yin {
  bottom: 0;
  background: radial-gradient(circle at 50% 0%, #1a1a2a 0%, #1a1a2a 25%, transparent 25%),
              radial-gradient(circle at 50% 100%, transparent 0%, transparent 25%, #1a1a2a 25%);
  background-size: 60px 60px, 60px 60px;
  background-position: 60px 0, 0 0;
  background-color: #1a1a2a;
  border-radius: 0 0 60px 60px;
}

.taiji-half .eye {
  position: absolute;
  width: 15px;
  height: 15px;
  border-radius: 50%;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.taiji-half.yang .eye {
  background: #1a1a2a;
}

.taiji-half.yin .eye {
  background: #e8e6e3;
}

/* 水墨晕染 */
.ink-wash-layer {
  position: absolute;
  width: 100%;
  height: 100%;
}

.ink-blob {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  animation: float 20s ease-in-out infinite;
}

.blob1 {
  width: 300px;
  height: 300px;
  top: -100px;
  left: -50px;
  background: radial-gradient(circle, rgba(212, 175, 55, 0.1) 0%, transparent 70%);
}

.blob2 {
  width: 400px;
  height: 400px;
  bottom: -150px;
  right: -100px;
  background: radial-gradient(circle, rgba(0, 168, 150, 0.08) 0%, transparent 70%);
  animation-delay: -7s;
}

.blob3 {
  width: 250px;
  height: 250px;
  top: 30%;
  right: 10%;
  background: radial-gradient(circle, rgba(42, 42, 58, 0.4) 0%, transparent 70%);
  animation-delay: -14s;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(30px, -30px) scale(1.1); }
  66% { transform: translate(-20px, 20px) scale(0.9); }
}

/* 光晕圈 */
.aura-rings {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.ring {
  position: absolute;
  border: 1px solid rgba(212, 175, 55, 0.1);
  border-radius: 50%;
  animation: expandRing 8s ease-out infinite;
}

.ring1 {
  width: 200px;
  height: 200px;
  top: -100px;
  left: -100px;
}

.ring2 {
  width: 300px;
  height: 300px;
  top: -150px;
  left: -150px;
  animation-delay: -2.6s;
}

.ring3 {
  width: 400px;
  height: 400px;
  top: -200px;
  left: -200px;
  animation-delay: -5.2s;
}

@keyframes expandRing {
  0% {
    transform: scale(0.5);
    opacity: 0.5;
    border-width: 2px;
  }
  100% {
    transform: scale(2);
    opacity: 0;
    border-width: 1px;
  }
}

/* 顶部装饰 */
.top-ornament {
  position: absolute;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  align-items: center;
  gap: 16px;
  opacity: 0.6;
}

.ornament-line {
  width: 60px;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--accent-gold), transparent);
}

.ornament-symbol {
  font-size: 24px;
  color: var(--accent-gold);
  animation: pulse 3s ease-in-out infinite;
}

/* 底部装饰 */
.bottom-ornament {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 24px;
  opacity: 0.3;
}

.hexagram-symbol {
  font-size: 20px;
  color: var(--accent-gold);
}

@keyframes pulse {
  0%, 100% { opacity: 0.6; }
  50% { opacity: 1; }
}
</style>
