<script setup lang="ts">
defineProps<{
  role: 'system' | 'user';
}>();
</script>

<template>
  <div class="message-bubble" :class="role">
    <slot />
  </div>
</template>

<style scoped>
.message-bubble {
  padding: 16px 20px;
  border-radius: 16px;
  font-size: 16px;
  line-height: 1.7;
  animation: fadeInUp 0.4s ease-out;
  backdrop-filter: blur(10px);
}

.message-bubble.system {
  background: rgba(20, 20, 32, 0.85);
  border: 1px solid rgba(212, 175, 55, 0.15);
  border-radius: 4px 16px 16px 16px;
  color: var(--text-primary);
  box-shadow: 
    0 4px 20px rgba(0, 0, 0, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.03);
}

.message-bubble.user {
  background: linear-gradient(135deg, 
    rgba(212, 175, 55, 0.9) 0%, 
    rgba(240, 216, 120, 0.9) 100%);
  color: var(--bg-primary);
  border-radius: 16px 16px 4px 16px;
  font-weight: 500;
  box-shadow: 
    0 4px 20px rgba(212, 175, 55, 0.3),
    0 0 30px rgba(212, 175, 55, 0.1);
}
</style>
