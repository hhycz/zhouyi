<script setup lang="ts">
import { ref, computed } from 'vue';

const emit = defineEmits<{
  submit: [info: {
    year: number;
    month: number;
    day: number;
    hour: number;
    minute: number;
    gender: 0 | 1;
  }]
}>();

const currentYear = new Date().getFullYear();
const form = ref({
  year: 1990,
  month: 1,
  day: 1,
  hour: 12,
  minute: 0,
  gender: 1 as 0 | 1
});

const years = computed(() => {
  const arr = [];
  for (let y = currentYear; y >= 1900; y--) {
    arr.push(y);
  }
  return arr;
});

const months = computed(() => Array.from({ length: 12 }, (_, i) => i + 1));

const days = computed(() => {
  const daysInMonth = new Date(form.value.year, form.value.month, 0).getDate();
  return Array.from({ length: daysInMonth }, (_, i) => i + 1);
});

const hours = computed(() => Array.from({ length: 24 }, (_, i) => i));

const minutes = computed(() => Array.from({ length: 60 }, (_, i) => i));

function handleSubmit() {
  emit('submit', { ...form.value });
}
</script>

<template>
  <div class="birth-date-form card">
    <div class="form-header">
      <span class="title">📜 生辰帖</span>
    </div>
    
    <div class="form-row">
      <label>性别</label>
      <div class="gender-toggle">
        <button 
          :class="{ active: form.gender === 1 }" 
          @click="form.gender = 1"
        >
          乾（男）
        </button>
        <button 
          :class="{ active: form.gender === 0 }" 
          @click="form.gender = 0"
        >
          坤（女）
        </button>
      </div>
    </div>
    
    <div class="form-row">
      <label>出生日期</label>
      <div class="date-inputs">
        <select v-model.number="form.year">
          <option v-for="y in years" :key="y" :value="y">{{ y }}年</option>
        </select>
        <select v-model.number="form.month">
          <option v-for="m in months" :key="m" :value="m">{{ m }}月</option>
        </select>
        <select v-model.number="form.day">
          <option v-for="d in days" :key="d" :value="d">{{ d }}日</option>
        </select>
      </div>
    </div>
    
    <div class="form-row">
      <label>出生时间</label>
      <div class="time-inputs">
        <select v-model.number="form.hour">
          <option v-for="h in hours" :key="h" :value="h">{{ h }}时</option>
        </select>
        <select v-model.number="form.minute">
          <option v-for="m in minutes" :key="m" :value="m">{{ String(m).padStart(2, '0') }}分</option>
        </select>
      </div>
    </div>
    
    <button class="submit-btn btn btn-primary" @click="handleSubmit">
      呈递生辰
    </button>
  </div>
</template>

<style scoped>
.birth-date-form {
  width: 100%;
  max-width: 400px;
  margin-top: 8px;
}

.form-header {
  text-align: center;
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--border-subtle);
}

.title {
  font-size: 18px;
  color: var(--accent-gold);
  letter-spacing: 4px;
}

.form-row {
  margin-bottom: 16px;
}

.form-row label {
  display: block;
  font-size: 14px;
  color: var(--text-secondary);
  margin-bottom: 8px;
}

.gender-toggle {
  display: flex;
  gap: 8px;
}

.gender-toggle button {
  flex: 1;
  padding: 12px;
  background: var(--bg-tertiary);
  border: 1px solid var(--border-subtle);
  border-radius: 8px;
  color: var(--text-primary);
  font-size: 15px;
  cursor: pointer;
  transition: all 0.2s;
}

.gender-toggle button.active {
  border-color: var(--accent-gold);
  color: var(--accent-gold);
  background: rgba(212, 175, 55, 0.1);
}

.date-inputs,
.time-inputs {
  display: flex;
  gap: 8px;
}

.date-inputs select,
.time-inputs select {
  flex: 1;
}

.submit-btn {
  width: 100%;
  margin-top: 20px;
  font-size: 16px;
  letter-spacing: 2px;
}
</style>
