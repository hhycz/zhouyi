<script setup lang="ts">
/**
 * 周易神秘背景组件 - 升级版
 * 包含八卦图、阴阳鱼、星辰连线、迷雾流云等装饰元素
 */
import { ref, onMounted, onUnmounted } from 'vue';

const baguaRotation = ref(0);
const mouseX = ref(0);
const mouseY = ref(0);
let animationId: number | null = null;

// 缓慢旋转八卦图
function animate() {
  baguaRotation.value += 0.03;
  animationId = requestAnimationFrame(animate);
}

// 鼠标视差效果
function handleMouseMove(e: MouseEvent) {
  const x = (e.clientX / window.innerWidth - 0.5) * 20;
  const y = (e.clientY / window.innerHeight - 0.5) * 20;
  mouseX.value = x;
  mouseY.value = y;
}

onMounted(() => {
  animate();
  window.addEventListener('mousemove', handleMouseMove);
});

onUnmounted(() => {
  if (animationId) {
    cancelAnimationFrame(animationId);
  }
  window.removeEventListener('mousemove', handleMouseMove);
});
</script>

<template>
  <div class="mystical-background">
    <!-- 深空背景底色 -->
    <div class="void-bg"></div>

    <!-- 迷雾层 -->
    <div class="fog-layer">
      <div class="fog fog-1"></div>
      <div class="fog fog-2"></div>
    </div>

    <!-- 星辰与连线层 -->
    <div class="constellation-layer" :style="{ transform: `translate(${mouseX * 0.5}px, ${mouseY * 0.5}px)` }">
      <!-- 随机星辰 -->
      <div v-for="i in 40" :key="`star-${i}`" class="star" :style="{
        left: `${Math.random() * 100}%`,
        top: `${Math.random() * 100}%`,
        animationDelay: `${Math.random() * 4}s`,
        opacity: Math.random() * 0.7 + 0.3,
        transform: `scale(${Math.random() * 0.5 + 0.5})`
      }"></div>
      
      <!-- 装饰性连线 (模拟星宿) -->
      <svg class="star-lines" width="100%" height="100%">
        <path d="M100,100 L200,150 L300,80" class="constellation-path" />
        <path d="M80%,20% L75%,30% L85%,40%" class="constellation-path" />
        <circle cx="100" cy="100" r="2" class="star-node" />
        <circle cx="200" cy="150" r="2" class="star-node" />
        <circle cx="300" cy="80" r="2" class="star-node" />
      </svg>
    </div>
    
    <!-- 八卦阵背景 -->
    <div class="bagua-layer" :style="{ transform: `translate(-50%, -50%) translate(${mouseX * 0.2}px, ${mouseY * 0.2}px)` }">
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
        <div class="taiji-wrapper">
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
    </div>
    
    <!-- 水墨流云层 -->
    <div class="ink-wash-layer" :style="{ transform: `translate(${mouseX * 0.8}px, ${mouseY * 0.8}px)` }">
      <div class="ink-blob blob1"></div>
      <div class="ink-blob blob2"></div>
      <div class="ink-blob blob3"></div>
    </div>
    
    <!-- 金色光晕圈 -->
    <div class="aura-rings">
      <div class="ring ring1"></div>
      <div class="ring ring2"></div>
    </div>
    
    <!-- 顶部装饰图案 -->
    <div class="top-ornament">
      <div class="ornament-line"></div>
      <span class="ornament-symbol">☯</span>
      <div class="ornament-line"></div>
    </div>
    
    <!-- 底部装饰 -->
    <div class="bottom-ornament">
      <div class="hex-row">
        <span class="hexagram-symbol">䷀</span>
        <span class="hexagram-symbol">䷁</span>
        <span class="hexagram-symbol">䷂</span>
        <span class="hexagram-symbol">䷃</span>
        <span class="hexagram-symbol">䷄</span>
      </div>
    </div>

    <!-- 前景噪点/暗角 -->
    <div class="vignette"></div>
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
  background-color: var(--bg-primary);
}

.void-bg {
  position: absolute;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at 50% 50%, #1a1b26 0%, #0a0a0f 100%);
  opacity: 0.8;
}

/* 迷雾效果 */
.fog-layer {
  position: absolute;
  width: 100%;
  height: 100%;
  opacity: 0.3;
  filter: blur(20px);
}

.fog {
  position: absolute;
  background: linear-gradient(to right, transparent, rgba(200, 200, 210, 0.1), transparent);
  width: 200%;
  height: 100%;
  animation: fogFlow 30s linear infinite;
}

.fog-1 { top: 0; animation-duration: 40s; }
.fog-2 { bottom: 0; animation-direction: reverse; animation-duration: 35s; }

@keyframes fogFlow {
  0% { transform: translateX(-50%); }
  100% { transform: translateX(0); }
}

/* 星辰粒子 */
.constellation-layer {
  position: absolute;
  width: 100%;
  height: 100%;
  transition: transform 0.1s ease-out;
}

.star {
  position: absolute;
  width: 2px;
  height: 2px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 50%;
  box-shadow: 0 0 4px rgba(255, 255, 255, 0.8);
  animation: twinkle 4s ease-in-out infinite;
}

.star-lines {
  position: absolute;
  opacity: 0.15;
}

.constellation-path {
  fill: none;
  stroke: var(--accent-gold);
  stroke-width: 1;
}

.star-node {
  fill: var(--accent-gold);
}

@keyframes twinkle {
  0%, 100% { opacity: 0.2; transform: scale(0.8); }
  50% { opacity: 0.8; transform: scale(1.2); }
}

/* 八卦阵 */
.bagua-layer {
  position: absolute;
  top: 50%;
  left: 50%;
  /* transform is handled inline for parallax */
  transition: transform 0.2s ease-out;
}

.bagua-container {
  position: relative;
  width: 500px;
  height: 500px;
  opacity: 0.06;
}

.bagua-symbols {
  position: absolute;
  width: 100%;
  height: 100%;
}

.trigram {
  position: absolute;
  font-size: 48px;
  color: var(--accent-gold);
  top: 50%;
  left: 50%;
  transform: rotate(var(--angle)) translateY(-220px) rotate(calc(-1 * var(--angle)));
  text-shadow: 0 0 15px rgba(212, 175, 55, 0.5);
}

/* 太极阴阳 */
.taiji-wrapper {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  filter: drop-shadow(0 0 30px rgba(212, 175, 55, 0.2));
}

.taiji {
  width: 160px;
  height: 160px;
  border-radius: 50%;
  position: relative;
  overflow: hidden;
  border: 1px solid rgba(212, 175, 55, 0.2);
}

.taiji-half {
  position: absolute;
  width: 100%;
  height: 50%;
}

.taiji-half.yang {
  top: 0;
  background: #e8e6e3;
  border-radius: 80px 80px 0 0;
}

.taiji-half.yang::before {
  content: '';
  position: absolute;
  bottom: -40px;
  right: 0;
  width: 80px;
  height: 80px;
  background: #e8e6e3;
  border-radius: 50%;
}

.taiji-half.yang::after {
  content: '';
  position: absolute;
  bottom: -40px;
  left: 0;
  width: 80px;
  height: 80px;
  background: #1a1a2a;
  border-radius: 50%;
}

.taiji-half.yin {
  bottom: 0;
  background: #1a1a2a;
  border-radius: 0 0 80px 80px;
}

.eye {
  position: absolute;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  z-index: 2;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  box-shadow: 0 0 10px rgba(0,0,0,0.2);
}

.yang .eye {
  background: #1a1a2a;
  top: 50%; /* Adjusted relative to parent */
  transform: translate(-50%, 20px); /* Manual adjustment for taiji geometry */
}

/* Override for pure CSS Taiji simplicity without complex pseudo elements if preferred, 
   but let's stick to the CSS gradient implementation as it was cleaner in V1. 
   Reverting to V1 gradient style for robustness but improved.
*/
.taiji {
  background: linear-gradient(to right, #e8e6e3 50%, #1a1a2a 50%);
}

.taiji-half.yang {
  width: 80px;
  height: 80px;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  background: #e8e6e3;
  border-radius: 50%;
  z-index: 1;
}

.taiji-half.yin {
  width: 80px;
  height: 80px;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  background: #1a1a2a;
  border-radius: 50%;
  z-index: 1;
}

.taiji-half.yang .eye { background: #1a1a2a; transform: translate(-50%, -50%); top: 50%; left: 50%; }
.taiji-half.yin .eye { background: #e8e6e3; transform: translate(-50%, -50%); top: 50%; left: 50%; }

/* 水墨晕染 */
.ink-wash-layer {
  position: absolute;
  width: 100%;
  height: 100%;
  transition: transform 0.4s ease-out;
}

.ink-blob {
  position: absolute;
  border-radius: 50%;
  filter: blur(90px);
  animation: float blobFloat 25s ease-in-out infinite;
  opacity: 0.6;
}

.blob1 {
  width: 400px;
  height: 400px;
  top: -10%;
  left: -5%;
  background: radial-gradient(circle, rgba(20, 20, 30, 0.9) 0%, transparent 70%);
}

.blob2 {
  width: 500px;
  height: 500px;
  bottom: -20%;
  right: -10%;
  background: radial-gradient(circle, rgba(10, 30, 40, 0.8) 0%, transparent 70%);
  animation-delay: -5s;
}

.blob3 {
  width: 300px;
  height: 300px;
  top: 40%;
  right: 20%;
  background: radial-gradient(circle, rgba(212, 175, 55, 0.05) 0%, transparent 70%);
  animation-delay: -12s;
}

@keyframes blobFloat {
  0%, 100% { transform: translate(0, 0) scale(1); }
  50% { transform: translate(20px, -20px) scale(1.05); }
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
  border: 1px solid rgba(212, 175, 55, 0.08);
  border-radius: 50%;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation: expandRing 10s linear infinite;
}

.ring1 { width: 300px; height: 300px; animation-duration: 12s; }
.ring2 { width: 500px; height: 500px; animation-delay: -6s; animation-duration: 15s; border-color: rgba(212, 175, 55, 0.04); }

@keyframes expandRing {
  0% { transform: translate(-50%, -50%) scale(0.8) rotate(0deg); opacity: 0; }
  50% { opacity: 0.5; }
  100% { transform: translate(-50%, -50%) scale(1.2) rotate(180deg); opacity: 0; }
}

/* 装饰 */
.top-ornament {
  position: absolute;
  top: 30px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  align-items: center;
  gap: 20px;
  opacity: 0.7;
}

.ornament-line {
  width: 100px;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--accent-gold), transparent);
}

.ornament-symbol {
  font-size: 28px;
  color: var(--accent-gold);
  text-shadow: 0 0 10px rgba(212, 175, 55, 0.5);
  animation: pulse 4s ease-in-out infinite;
}

.bottom-ornament {
  position: absolute;
  bottom: 30px;
  left: 0;
  width: 100%;
  display: flex;
  justify-content: center;
  opacity: 0.25;
}

.hex-row {
  display: flex;
  gap: 30px;
}

.hexagram-symbol {
  font-size: 24px;
  color: var(--accent-gold);
  filter: blur(0.5px);
}

.vignette {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at center, transparent 40%, #0a0a0f 120%);
  pointer-events: none;
}
</style>
