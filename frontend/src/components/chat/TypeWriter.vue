<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';

const props = withDefaults(defineProps<{
  text: string;
  delay?: number;
}>(), {
  delay: 40
});

const displayedText = ref('');
const isComplete = ref(false);

onMounted(() => {
  let index = 0;
  const interval = setInterval(() => {
    if (index < props.text.length) {
      displayedText.value += props.text[index];
      index++;
    } else {
      clearInterval(interval);
      isComplete.value = true;
    }
  }, props.delay);
});
</script>

<template>
  <span class="typewriter">
    {{ displayedText }}
    <span v-if="!isComplete" class="cursor">|</span>
  </span>
</template>

<style scoped>
.typewriter {
  display: inline;
}

.cursor {
  animation: blink 1s step-end infinite;
  color: var(--accent-gold);
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}
</style>
