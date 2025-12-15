<script setup lang="ts">
import { ref, onMounted } from 'vue';

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
    <span v-if="!isComplete" class="cursor"></span>
  </span>
</template>

<style scoped>
.typewriter {
  display: inline;
}

.cursor {
  display: inline-block;
  width: 0.5em;
  height: 1em;
  background-color: var(--accent-gold);
  vertical-align: text-bottom;
  animation: blink 0.8s step-end infinite;
  opacity: 0.8;
  margin-left: 2px;
  box-shadow: 0 0 5px var(--accent-gold);
}

@keyframes blink {
  0%, 100% { opacity: 0.8; }
  50% { opacity: 0; }
}
</style>
