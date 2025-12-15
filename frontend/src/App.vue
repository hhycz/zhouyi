<script setup lang="ts">
import ChatContainer from './components/chat/ChatContainer.vue';
import MysticalBackground from './components/background/MysticalBackground.vue';
</script>

<template>
  <div class="app-container">
    <MysticalBackground />
    <ChatContainer />
  </div>
</template>

<style>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@300;400;500;600&display=swap');

.app-container {
  position: relative;
  width: 100%;
  height: 100%;
}
</style>

