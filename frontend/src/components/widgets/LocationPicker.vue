<script setup lang="ts">
import { ref } from 'vue';

const emit = defineEmits<{
  select: [location: { city: string; longitude: number; latitude: number }]
}>();

const cityInput = ref('');
const isSearching = ref(false);

// 预设城市数据（简化版，实际可接入地图API）
const commonCities = [
  { city: '北京', longitude: 116.4, latitude: 39.9 },
  { city: '上海', longitude: 121.5, latitude: 31.2 },
  { city: '广州', longitude: 113.3, latitude: 23.1 },
  { city: '深圳', longitude: 114.1, latitude: 22.5 },
  { city: '杭州', longitude: 120.2, latitude: 30.3 },
  { city: '南京', longitude: 118.8, latitude: 32.1 },
  { city: '成都', longitude: 104.1, latitude: 30.7 },
  { city: '重庆', longitude: 106.5, latitude: 29.6 },
  { city: '武汉', longitude: 114.3, latitude: 30.6 },
  { city: '西安', longitude: 108.9, latitude: 34.3 },
  { city: '苏州', longitude: 120.6, latitude: 31.3 },
  { city: '天津', longitude: 117.2, latitude: 39.1 },
];

function selectCity(cityData: { city: string; longitude: number; latitude: number }) {
  emit('select', cityData);
}

function searchCity() {
  if (!cityInput.value.trim()) return;
  
  // 在预设列表中查找
  const found = commonCities.find(c => c.city.includes(cityInput.value));
  if (found) {
    emit('select', found);
  } else {
    // 默认使用北京经度作为参考
    emit('select', {
      city: cityInput.value,
      longitude: 116.4,
      latitude: 39.9
    });
  }
}
</script>

<template>
  <div class="location-picker card">
    <div class="search-bar">
      <input 
        v-model="cityInput"
        type="text" 
        placeholder="输入城市名..."
        @keyup.enter="searchCity"
      />
      <button class="btn btn-primary" @click="searchCity">确定</button>
    </div>
    
    <div class="quick-cities">
      <span class="label">常用城市：</span>
      <div class="city-tags">
        <button 
          v-for="city in commonCities.slice(0, 8)" 
          :key="city.city"
          class="city-tag"
          @click="selectCity(city)"
        >
          {{ city.city }}
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.location-picker {
  width: 100%;
  max-width: 400px;
  margin-top: 8px;
}

.search-bar {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
}

.search-bar input {
  flex: 1;
}

.search-bar .btn {
  padding: 12px 20px;
}

.quick-cities .label {
  display: block;
  font-size: 13px;
  color: var(--text-secondary);
  margin-bottom: 10px;
}

.city-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.city-tag {
  padding: 8px 16px;
  background: var(--bg-tertiary);
  border: 1px solid var(--border-subtle);
  border-radius: 20px;
  color: var(--text-primary);
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.city-tag:hover {
  border-color: var(--accent-jade);
  color: var(--accent-jade);
}
</style>
