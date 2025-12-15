<script setup lang="ts">
import type { IntentType } from '@/types';

const emit = defineEmits<{
  select: [intent: IntentType]
}>();

const intents: { type: IntentType; label: string; icon: string; desc: string }[] = [
  { type: 'career', label: '问前程', icon: '📈', desc: '事业 · 学业 · 财运' },
  { type: 'love', label: '问姻缘', icon: '💕', desc: '感情 · 桃花 · 婚姻' },
  { type: 'fortune', label: '问吉凶', icon: '🔮', desc: '健康 · 流年 · 运势' }
];
</script>

<template>
  <div class="intent-selector">
    <button 
      v-for="intent in intents" 
      :key="intent.type"
      class="intent-card"
      @click="emit('select', intent.type)"
    >
      <span class="icon">{{ intent.icon }}</span>
      <span class="label">{{ intent.label }}</span>
      <span class="desc">{{ intent.desc }}</span>
    </button>
  </div>
</template>

<style scoped>
.intent-selector {
  display: flex;
  gap: 12px;
  margin-top: 8px;
  flex-wrap: wrap;
}

.intent-card {
  flex: 1;
  min-width: 120px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 20px 16px;
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.intent-card:hover {
  border-color: var(--accent-gold);
  transform: translateY(-4px);
  box-shadow: var(--shadow-glow);
}

.icon {
  font-size: 32px;
}

.label {
  font-size: 18px;
  color: var(--accent-gold);
  font-weight: 500;
  letter-spacing: 2px;
}

.desc {
  font-size: 12px;
  color: var(--text-secondary);
}
</style>
