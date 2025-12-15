<script setup lang="ts">
defineProps<{
  role: 'system' | 'user';
}>();
</script>

<template>
  <div class="message-bubble" :class="role">
    <div class="content">
        <slot />
    </div>
    <!-- 装饰性角标 -->
    <div v-if="role === 'system'" class="corner-decor top-left"></div>
    <div v-if="role === 'system'" class="corner-decor bottom-right"></div>
  </div>
</template>

<style scoped>
.message-bubble {
  position: relative;
  padding: 18px 24px;
  border-radius: 12px;
  font-size: 16px;
  line-height: 1.8;
  animation: fadeInUp 0.5s cubic-bezier(0.2, 0.8, 0.2, 1);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  max-width: 100%;
}

/* 系统消息 - 水墨/毛边纸风格 */
.message-bubble.system {
  background: rgba(22, 24, 33, 0.85);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 4px 16px 16px 16px;
  color: var(--text-primary);
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.3),
    inset 0 0 20px rgba(0, 0, 0, 0.2);
  border-left: 2px solid var(--accent-gold);
}

/* 系统消息装饰角 */
.corner-decor {
    position: absolute;
    width: 6px;
    height: 6px;
    border: 1px solid var(--accent-gold);
    opacity: 0.5;
}

.corner-decor.top-left {
    top: 4px;
    left: 4px;
    border-right: none;
    border-bottom: none;
}

.corner-decor.bottom-right {
    bottom: 4px;
    right: 4px;
    border-left: none;
    border-top: none;
}

/* 用户消息 - 金箔/印章风格 */
.message-bubble.user {
  background: linear-gradient(135deg, 
    var(--accent-gold) 0%, 
    var(--accent-gold-light) 100%);
  color: #1a1a2a; /* 深色文字 */
  border-radius: 16px 16px 4px 16px;
  font-weight: 600;
  box-shadow: 
    0 4px 20px rgba(212, 175, 55, 0.3),
    0 0 15px rgba(212, 175, 55, 0.2);
  text-shadow: 0 1px 0 rgba(255,255,255,0.4);
  letter-spacing: 0.5px;
}

.content {
  position: relative;
  z-index: 1;
}

/* 进入动画 */
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px) scale(0.98); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}
</style>
