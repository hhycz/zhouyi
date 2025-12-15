<script setup lang="ts">
import type { BaziResponse } from '@/types';

const props = defineProps<{
  data: BaziResponse;
}>();

// 五行颜色映射
const elementColors: Record<string, string> = {
  '木': 'var(--element-wood)',
  '火': 'var(--element-fire)',
  '土': 'var(--element-earth)',
  '金': 'var(--element-metal)',
  '水': 'var(--element-water)'
};

function getElementColor(element: string) {
  return elementColors[element] || 'var(--text-primary)';
}
</script>

<template>
  <div class="bazi-chart card-glow">
    <!-- 基本信息 -->
    <div class="chart-header">
      <div class="info-item">
        <span class="label">农历</span>
        <span class="value">{{ data.birth_info.lunar_date }}</span>
      </div>
      <div class="info-item">
        <span class="label">生肖</span>
        <span class="value">{{ data.additional_info.zodiac }}</span>
      </div>
      <div class="info-item">
        <span class="label">星座</span>
        <span class="value">{{ data.additional_info.constellation }}</span>
      </div>
    </div>
    
    <!-- 四柱 -->
    <div class="pillars">
      <div 
        v-for="pillar in data.chart.pillars" 
        :key="pillar.position"
        class="pillar"
      >
        <div class="pillar-label">{{ pillar.position_cn }}</div>
        <div class="pillar-content">
          <div 
            class="gan" 
            :style="{ color: getElementColor(pillar.gan_element) }"
          >
            {{ pillar.gan }}
          </div>
          <div 
            class="zhi"
            :style="{ color: getElementColor(pillar.zhi_element) }"
          >
            {{ pillar.zhi }}
          </div>
        </div>
        <div class="ten-god">{{ pillar.ten_god }}</div>
        <div class="hidden-stems">
          <span 
            v-for="(stem, idx) in pillar.hidden_stems" 
            :key="idx"
            class="hidden-stem"
          >
            {{ stem }}
          </span>
        </div>
        <div class="nayin">{{ pillar.nayin }}</div>
      </div>
    </div>
    
    <!-- 五行统计 -->
    <div class="elements-section">
      <div class="section-title">五行分布</div>
      <div class="elements-bar">
        <div 
          v-for="(count, element) in data.chart.elements_count" 
          :key="element as string"
          class="element-item"
          :style="{ 
            backgroundColor: getElementColor(element as string),
            width: `${(count as number / 8) * 100}%` 
          }"
        >
          <span>{{ element }}{{ count }}</span>
        </div>
      </div>
    </div>
    
    <!-- 大运 -->
    <div class="luck-section" v-if="data.luck_cycles.length > 0">
      <div class="section-title">大运流年</div>
      <div class="luck-cycles">
        <div 
          v-for="cycle in data.luck_cycles.slice(0, 6)" 
          :key="cycle.index"
          class="luck-item"
        >
          <span class="age">{{ cycle.start_age }}-{{ cycle.end_age }}岁</span>
          <span class="ganzhi">{{ cycle.gan_zhi }}</span>
          <span class="years">{{ cycle.start_year }}-{{ cycle.end_year }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.bazi-chart {
  width: 100%;
  max-width: 500px;
  margin-top: 12px;
  padding: 24px;
  background: var(--bg-card);
  border: 1px solid var(--border-accent);
  border-radius: 16px;
}

.chart-header {
  display: flex;
  justify-content: space-around;
  padding-bottom: 16px;
  margin-bottom: 20px;
  border-bottom: 1px solid var(--border-subtle);
}

.info-item {
  text-align: center;
}

.info-item .label {
  display: block;
  font-size: 12px;
  color: var(--text-secondary);
  margin-bottom: 4px;
}

.info-item .value {
  font-size: 14px;
  color: var(--accent-gold);
}

/* 四柱布局 */
.pillars {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-bottom: 24px;
}

.pillar {
  flex: 1;
  max-width: 80px;
  text-align: center;
}

.pillar-label {
  font-size: 12px;
  color: var(--text-secondary);
  margin-bottom: 8px;
}

.pillar-content {
  background: var(--bg-tertiary);
  border: 1px solid var(--border-subtle);
  border-radius: 8px;
  padding: 12px 8px;
  margin-bottom: 8px;
}

.gan, .zhi {
  font-size: 28px;
  font-weight: 500;
  line-height: 1.3;
}

.ten-god {
  font-size: 12px;
  color: var(--accent-jade);
  margin-bottom: 6px;
}

.hidden-stems {
  display: flex;
  justify-content: center;
  gap: 4px;
  margin-bottom: 6px;
}

.hidden-stem {
  font-size: 11px;
  color: var(--text-muted);
  padding: 2px 4px;
  background: var(--bg-tertiary);
  border-radius: 4px;
}

.nayin {
  font-size: 10px;
  color: var(--text-muted);
}

/* 五行分布 */
.section-title {
  font-size: 14px;
  color: var(--text-secondary);
  margin-bottom: 12px;
  text-align: center;
}

.elements-bar {
  display: flex;
  border-radius: 8px;
  overflow: hidden;
  height: 32px;
}

.element-item {
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 40px;
  transition: all 0.3s;
}

.element-item span {
  font-size: 12px;
  color: white;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
}

/* 大运 */
.luck-section {
  margin-top: 20px;
  padding-top: 16px;
  border-top: 1px solid var(--border-subtle);
}

.luck-cycles {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.luck-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 8px 12px;
  background: var(--bg-tertiary);
  border-radius: 8px;
  font-size: 12px;
  gap: 4px;
}

.luck-item .age {
  color: var(--text-secondary);
}

.luck-item .ganzhi {
  font-size: 16px;
  color: var(--accent-gold);
}

.luck-item .years {
  font-size: 10px;
  color: var(--text-muted);
}
</style>
