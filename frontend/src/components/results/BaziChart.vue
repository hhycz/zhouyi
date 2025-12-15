<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { api } from '@/api';
import type { BaziResponse, BaziRequest, LuckCycle, LiuNian } from '@/types';

const props = defineProps<{
  data: BaziResponse;
}>();

// 状态控制
const isExpanded = ref(false); // 放大查看模式
const selectedLuckCycle = ref<LuckCycle | null>(null); // 当前选中的大运
const analyzingYear = ref<number | null>(null); // 正在分析的年份
const yearAnalysisContent = ref<string | null>(null); // 年运分析结果

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

function toggleExpand() {
    isExpanded.value = !isExpanded.value;
}

function selectLuckCycle(cycle: LuckCycle) {
    selectedLuckCycle.value = cycle;
}

// AI 解读相关
const isAILoading = ref(false);
const aiContent = ref('');
const aiError = ref('');

async function requestAIInterpretation() {
    isAILoading.value = true;
    aiError.value = '';
    
    try {
        const birthDate = new Date(props.data.birth_info.solar_date);
        const req: BaziRequest = {
            birth_year: birthDate.getFullYear(),
            birth_month: birthDate.getMonth() + 1,
            birth_day: birthDate.getDate(),
            birth_hour: birthDate.getHours(),
            birth_minute: birthDate.getMinutes(),
            longitude: props.data.birth_info.longitude,
            latitude: props.data.birth_info.latitude,
            gender: props.data.birth_info.gender === '男' ? 1 : 0,
            use_true_solar_time: !!props.data.birth_info.true_solar_time
        };
        
        const result = await api.getBaziAIInterpretation(req);
        if (result.success) {
            aiContent.value = result.content;
        } else {
            aiError.value = 'AI 解读失败，请稍后重试';
        }
    } catch (err: any) {
        aiError.value = err.message || '网络请求错误';
    } finally {
        isAILoading.value = false;
    }
}

// 流年分析
async function handleYearClick(year: LiuNian) {
    if (analyzingYear.value === year.year) return;
    
    analyzingYear.value = year.year;
    yearAnalysisContent.value = null;
    
    try {
        const birthDate = new Date(props.data.birth_info.solar_date);
        const req: BaziRequest = {
            birth_year: birthDate.getFullYear(),
            birth_month: birthDate.getMonth() + 1,
            birth_day: birthDate.getDate(),
            birth_hour: birthDate.getHours(),
            birth_minute: birthDate.getMinutes(),
            longitude: props.data.birth_info.longitude,
            latitude: props.data.birth_info.latitude,
            gender: props.data.birth_info.gender === '男' ? 1 : 0,
            use_true_solar_time: !!props.data.birth_info.true_solar_time
        };
        
        const result = await api.analyzeBaziYear(req, year.year);
        if (result.success) {
            yearAnalysisContent.value = result.content;
        } else {
            yearAnalysisContent.value = "分析失败，请重试。";
        }
    } catch (err) {
        yearAnalysisContent.value = "网络请求失败";
    } finally {
        // Stop loading state is implicit by content presence, 
        // but we keep analyzingYear active to show the modal
    }
}

function closeYearAnalysis() {
    analyzingYear.value = null;
    yearAnalysisContent.value = null;
}

const maxElementCount = computed(() => {
    const counts = Object.values(props.data.chart.elements_count);
    return Math.max(...counts, 1);
});

const strengthPercent = computed(() => {
    const score = props.data.strength_analysis?.score || 0;
    let p = (score + 50); 
    if (p < 0) p = 0; 
    if (p > 100) p = 100;
    return p;
});

const strengthColor = computed(() => {
    const score = props.data.strength_analysis?.score || 0;
    if (score >= 20) return 'var(--accent-cinnabar)'; 
    if (score <= -20) return 'var(--accent-jade)'; 
    return 'var(--accent-gold)'; 
});

// Auto-select current luck cycle on mount
onMounted(() => {
    if (props.data.luck_cycles && props.data.luck_cycles.length > 0) {
        const currentYear = new Date().getFullYear();
        const currentCycle = props.data.luck_cycles.find(c => currentYear >= c.start_year && currentYear <= c.end_year);
        
        if (currentCycle) {
            selectedLuckCycle.value = currentCycle;
        } else if (props.data.luck_cycles.length > 1) {
            selectedLuckCycle.value = props.data.luck_cycles[0];
        }
    }
});
</script>

<template>
  <div class="bazi-chart card-glow fade-in-up" :class="{ 'expanded': isExpanded }">
    <!-- 放大/缩小按钮 -->
    <button class="expand-btn" @click="toggleExpand" :title="isExpanded ? '缩小' : '全屏查看'">
        <span v-if="isExpanded">↙</span>
        <span v-else>↗</span>
    </button>
    
    <!-- 滚动容器 -->
    <div class="chart-scroll-container">
    
        <!-- 头部基本信息 -->
        <div class="chart-header">
        <div class="info-row main-info">
            <span class="gender">{{ data.birth_info.gender }}命</span>
            <span class="lunar">{{ data.birth_info.lunar_date }}</span>
        </div>
        <div class="info-row sub-info">
            <span>生肖: {{ data.additional_info.zodiac }}</span>
            <span>星座: {{ data.additional_info.constellation }}</span>
        </div>
        </div>
        
        <!-- 核心分析面板 -->
        <div class="analysis-panel paper-texture" v-if="data.strength_analysis">
        <div class="panel-row">
            <div class="strength-box">
                <div class="label">身强弱</div>
                <div class="value" :style="{ color: strengthColor }">{{ data.strength_analysis.level }}</div>
                <div class="progress-bar">
                    <div class="progress-fill" :style="{ width: strengthPercent + '%', background: strengthColor }"></div>
                </div>
            </div>
            
            <div class="pattern-box">
                <div class="label">格局</div>
                <div class="value highlight">
                    {{ data.pattern_analysis?.main_pattern?.name || '未入正格' }}
                </div>
            </div>
        </div>
        
        <div class="panel-row useful-gods" v-if="data.useful_gods">
            <div class="god-tag user-god" v-if="data.useful_gods.yong_shen">
                <span class="tag-label">用</span>
                <span class="tag-val" :style="{ color: getElementColor(data.useful_gods.yong_shen) }">{{ data.useful_gods.yong_shen }}</span>
            </div>
            <div class="god-tag xi-god" v-for="xi in data.useful_gods.xi_shen" :key="xi">
                <span class="tag-label">喜</span>
                <span class="tag-val" :style="{ color: getElementColor(xi) }">{{ xi }}</span>
            </div>
            <div class="god-tag tiao-hou" v-if="data.useful_gods.tiao_hou">
                <span class="tag-label">调</span>
                <span class="tag-val">{{ data.useful_gods.tiao_hou.split(' ')[0] }}</span>
            </div>
        </div>
        </div>
        
        <!-- 四柱 -->
        <div class="pillars">
        <div 
            v-for="pillar in data.chart.pillars" 
            :key="pillar.position"
            class="pillar"
        >
            <div class="pillar-head">{{ pillar.position_cn }}</div>
            <div class="pillar-body">
            <div class="ten-god-top">{{ pillar.ten_god }}</div>
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
            <div class="hidden-stems">
                <div v-for="stem in pillar.hidden_stems" :key="stem" class="stem-char">
                    {{ stem }}
                </div>
            </div>
            </div>
            <div class="nayin">{{ pillar.nayin }}</div>
        </div>
        </div>
        
        <!-- 五行能量 -->
        <div class="elements-section">
        <div class="section-title">五行能量分布</div>
        <div class="elements-chart">
            <div 
            v-for="(count, element) in data.chart.elements_count" 
            :key="element as string"
            class="element-bar-group"
            >
            <div class="bar-track">
                <div 
                    class="bar-fill"
                    :style="{ 
                        height: `${(count as number / maxElementCount) * 100}%`,
                        backgroundColor: getElementColor(element as string)
                    }"
                ></div>
            </div>
            <div class="element-label" :style="{ color: getElementColor(element as string) }">
                {{ element }}{{ count }}
            </div>
            </div>
        </div>
        </div>
        
        <!-- 大运与流年 (互动区域) -->
        <div class="luck-section">
        <div class="section-title">大运排盘 <span class="hint">(点击选中查看详情)</span></div>
        <div class="luck-scroll">
            <div 
            v-for="cycle in data.luck_cycles" 
            :key="cycle.index"
            class="luck-card"
            :class="{ 'active': selectedLuckCycle?.index === cycle.index }"
            @click="selectLuckCycle(cycle)"
            >
            <div class="ganzhi">{{ cycle.gan_zhi }}</div>
            <div class="age">{{ cycle.start_age }}岁</div>
            <div class="year">{{ cycle.start_year }}</div>
            </div>
        </div>
        
        <!-- 流年详情展示 -->
        <div v-if="selectedLuckCycle" class="liunian-panel fade-in-up">
            <div class="liunian-title">
                {{ selectedLuckCycle.gan_zhi }}大运 ({{ selectedLuckCycle.start_year }}~{{ selectedLuckCycle.end_year }}) 流年
                <span class="hint-small">点击年份查看吉凶分析</span>
            </div>
            <div class="liunian-grid">
                <div 
                    v-for="year in selectedLuckCycle.years" 
                    :key="year.year" 
                    class="liunian-item interactable"
                    @click="handleYearClick(year)"
                >
                    <div class="ln-year">{{ year.year }}</div>
                    <div class="ln-age">{{ year.age }}岁</div>
                    <div class="ln-ganzhi">{{ year.gan_zhi }}</div>
                    <div class="ln-god">{{ year.ten_god }}</div>
                    <!-- 事件标记 -->
                    <div class="ln-events" v-if="year.events && year.events.length">
                        <span v-for="evt in year.events.slice(0, 2)" :key="evt" class="evt-badge" :class="{'bad': evt.includes('冲') || evt.includes('刑'), 'good': evt.includes('合')}">
                            {{ evt[0] }}
                        </span>
                    </div>
                </div>
            </div>
        </div>
        </div>
        
        <!-- AI 解读区域 -->
        <div class="ai-section">
        <button 
            v-if="!aiContent && !isAILoading" 
            class="ai-btn" 
            @click="requestAIInterpretation"
        >
            <span class="sparkle">✨</span> AI 深度批命
        </button>
        
        <div v-if="isAILoading" class="ai-loading">
            <div class="loading-spinner"></div>
            <span>正在推演天机...</span>
        </div>
        
        <div v-if="aiError" class="ai-error">
            {{ aiError }}
        </div>
        
        <div v-if="aiContent" class="ai-content paper-texture">
            <div class="section-title">🤖 AI 命理批注</div>
            <div class="ai-text" v-html="aiContent.replace(/\n/g, '<br>')"></div>
        </div>
        </div>
    
    </div>
  </div>
  
  <!-- 全屏遮罩 -->
  <div v-if="isExpanded" class="modal-overlay" @click="toggleExpand"></div>
  
  <!-- 流年分析遮罩 (特定年份) -->
  <div v-if="analyzingYear" class="year-modal-overlay" @click.self="closeYearAnalysis">
      <div class="year-modal-content card-glow">
          <button class="close-btn" @click="closeYearAnalysis">×</button>
          <div class="modal-title">{{ analyzingYear }}年 流年运势分析</div>
          
          <div v-if="!yearAnalysisContent" class="loading-box">
             <div class="loading-spinner"></div>
             <p>AI 正在推演该年吉凶...</p>
          </div>
          
          <div v-else class="modal-body paper-texture" v-html="yearAnalysisContent.replace(/\n/g, '<br>')">
          </div>
      </div>
  </div>
</template>

<style scoped>
.bazi-chart {
  width: 100%;
  max-width: 480px;
  padding: 24px;
  background: var(--bg-card);
  border: 1px solid var(--border-accent);
  border-radius: 12px;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
}

/* 全屏放大模式 */
.bazi-chart.expanded {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 90vw;
    max-width: 800px;
    height: 90vh;
    z-index: 1000;
    overflow: hidden; /* 内容内部滚动 */
    display: flex;
    flex-direction: column;
}

.chart-scroll-container {
    height: 100%;
    overflow-y: auto;
    padding-right: 4px;
}

.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0,0,0,0.8);
    backdrop-filter: blur(5px);
    z-index: 999;
}

.expand-btn {
    position: absolute;
    top: 10px;
    right: 10px;
    background: rgba(0,0,0,0.3);
    border: 1px solid var(--border-subtle);
    color: var(--accent-gold);
    width: 32px;
    height: 32px;
    border-radius: 50%;
    cursor: pointer;
    z-index: 1010; /* 高于内容 */
    display: flex;
    align-items: center;
    justify-content: center;
}
.expand-btn:hover {
    background: var(--accent-gold);
    color: #000;
}

.paper-texture {
    background: rgba(255, 255, 255, 0.02);
    box-shadow: inset 0 0 20px rgba(0,0,0,0.2);
    border-radius: 8px;
}

/* 头部 */
.chart-header {
  text-align: center;
  margin-bottom: 20px;
  border-bottom: 1px solid var(--border-subtle);
  padding-bottom: 16px;
}
.main-info {
    font-size: 18px;
    font-weight: bold;
    color: var(--accent-gold);
    margin-bottom: 8px;
}
.gender { margin-right: 12px; }
.sub-info {
    font-size: 13px;
    color: var(--text-secondary);
    display: flex;
    justify-content: center;
    gap: 16px;
}

/* 核心分析面板 */
.analysis-panel {
    padding: 16px;
    margin-bottom: 24px;
    border: 1px solid var(--border-subtle);
}

.panel-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
}

.strength-box, .pattern-box {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.label {
    font-size: 12px;
    color: var(--text-muted);
    margin-bottom: 4px;
}

.value {
    font-size: 16px;
    font-weight: bold;
}

.progress-bar {
    width: 80%;
    height: 4px;
    background: #333;
    border-radius: 2px;
    margin-top: 4px;
    overflow: hidden;
    position: relative;
}
.progress-bar::after {
    content: '';
    position: absolute;
    left: 50%;
    top: 0;
    bottom: 0;
    width: 1px;
    background: rgba(255,255,255,0.3);
}

.progress-fill {
    height: 100%;
    transition: width 0.5s ease;
}

.highlight {
    color: var(--accent-gold);
    text-shadow: 0 0 5px rgba(212, 175, 55, 0.3);
}

.useful-gods {
    justify-content: center;
    gap: 8px;
    margin-bottom: 0;
}

.god-tag {
    display: flex;
    align-items: center;
    border: 1px solid var(--border-subtle);
    border-radius: 4px;
    padding: 2px 6px;
    font-size: 12px;
    background: rgba(0,0,0,0.2);
}

.tag-label {
    color: var(--text-muted);
    margin-right: 4px;
    font-size: 10px;
}
.tag-val {
    font-weight: bold;
}

/* 四柱 */
.pillars {
  display: flex;
  justify-content: space-between;
  margin-bottom: 24px;
  gap: 8px;
}

.pillar {
  flex: 1;
  text-align: center;
  background: var(--bg-tertiary);
  border-radius: 8px;
  padding: 12px 4px;
  border: 1px solid transparent;
  transition: border-color 0.3s;
}
.pillar:hover {
    border-color: var(--accent-gold-dim);
}

.pillar-head {
    font-size: 12px;
    color: var(--text-secondary);
    margin-bottom: 8px;
}

.ten-god-top {
    font-size: 10px;
    color: var(--text-muted);
    height: 14px;
}

.gan, .zhi {
    font-size: 24px;
    font-weight: bold;
    font-family: 'KaiTi', serif;
    line-height: 1.4;
}

.hidden-stems {
    display: flex;
    justify-content: center;
    gap: 2px;
    margin-top: 4px;
    height: 16px;
}
.stem-char {
    font-size: 10px;
    color: var(--text-muted);
    opacity: 0.7;
}

.nayin {
    font-size: 10px;
    color: var(--text-muted);
    margin-top: 8px;
    transform: scale(0.9);
}

/* 五行能量图 */
.elements-chart {
    display: flex;
    justify-content: space-around;
    align-items: flex-end;
    height: 100px;
    padding: 10px 0;
    margin-bottom: 20px;
    border-bottom: 1px solid var(--border-subtle);
}

.element-bar-group {
    display: flex;
    flex-direction: column;
    align-items: center;
    height: 100%;
    width: 30px;
}

.bar-track {
    flex: 1;
    width: 6px;
    background: rgba(255,255,255,0.05);
    border-radius: 3px;
    position: relative;
    display: flex;
    align-items: flex-end;
}

.bar-fill {
    width: 100%;
    border-radius: 3px;
    transition: height 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.element-label {
    margin-top: 6px;
    font-size: 12px;
}

/* 大运 */
.luck-section {
    margin-bottom: 20px;
}
.hint {
    font-size: 11px;
    color: var(--text-muted);
    font-weight: normal;
    margin-left: 8px;
}

.luck-scroll {
    display: flex;
    overflow-x: auto;
    gap: 12px;
    padding-bottom: 8px;
    scrollbar-width: thin;
    scrollbar-color: var(--accent-gold-dim) transparent;
}

.luck-card {
    min-width: 60px;
    padding: 10px;
    background: rgba(255,255,255,0.03);
    border: 1px solid var(--border-subtle);
    border-radius: 6px;
    text-align: center;
    cursor: pointer;
    transition: all 0.2s;
}

.luck-card:hover {
    border-color: var(--accent-gold-dim);
    background: rgba(255,255,255,0.05);
}

.luck-card.active {
    border-color: var(--accent-gold);
    background: rgba(212, 175, 55, 0.1);
    box-shadow: 0 0 10px rgba(212, 175, 55, 0.2);
}

.luck-card .ganzhi {
    font-size: 18px;
    color: var(--accent-gold);
    margin-bottom: 4px;
}
.luck-card .age, .luck-card .year {
    font-size: 10px;
    color: var(--text-muted);
}

/* 流年面板 */
.liunian-panel {
    margin-top: 16px;
    background: rgba(0,0,0,0.2);
    border-radius: 8px;
    padding: 12px;
    border: 1px solid var(--border-subtle);
}

.liunian-title {
    font-size: 14px;
    color: var(--text-secondary);
    margin-bottom: 12px;
    text-align: center;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    padding-bottom: 8px;
}
.hint-small {
    display: block;
    margin-top: 4px;
    font-size: 10px;
    color: var(--text-muted);
    opacity: 0.8;
}

.liunian-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 8px;
}

.liunian-item {
    text-align: center;
    padding: 6px 2px;
    background: rgba(255,255,255,0.02);
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.2s;
    position: relative;
    border: 1px solid transparent;
}
.liunian-item:hover {
    background: rgba(255,255,255,0.08);
    border-color: var(--accent-gold-dim);
}

.ln-year { font-size: 10px; color: var(--text-muted); }
.ln-age { font-size: 10px; color: var(--text-muted); margin-bottom: 2px;}
.ln-ganzhi { font-size: 14px; color: var(--accent-gold); font-weight: bold; }
.ln-god { font-size: 10px; color: var(--text-secondary); }

.ln-events {
    display: flex;
    justify-content: center;
    gap: 2px;
    margin-top: 4px;
    min-height: 12px;
}
.evt-badge {
    font-size: 9px;
    padding: 1px 3px;
    border-radius: 2px;
    background: rgba(255,255,255,0.1);
    color: var(--text-muted);
}
.evt-badge.bad { background: rgba(255, 80, 80, 0.2); color: #ff8080; }
.evt-badge.good { background: rgba(80, 255, 120, 0.2); color: #80ff90; }


/* AI 区域 */
.ai-section {
    margin-top: 24px;
}

.ai-btn {
  width: 100%;
  padding: 14px;
  background: linear-gradient(135deg, rgba(212, 175, 55, 0.15) 0%, rgba(0, 168, 150, 0.15) 100%);
  border: 1px solid var(--border-accent);
  border-radius: 8px;
  color: var(--accent-gold);
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.ai-btn:hover {
  background: linear-gradient(135deg, rgba(212, 175, 55, 0.25) 0%, rgba(0, 168, 150, 0.25) 100%);
  box-shadow: 0 0 15px rgba(212, 175, 55, 0.2);
}

.ai-text {
    font-size: 15px;
    line-height: 1.8;
    color: var(--text-primary);
    text-align: justify;
    padding: 16px;
}

.section-title {
    font-size: 14px;
    color: var(--text-secondary);
    margin-bottom: 12px;
    padding-left: 8px;
    border-left: 2px solid var(--accent-gold);
}

/* Year Modal */
.year-modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0,0,0,0.85);
    z-index: 2000;
    display: flex;
    align-items: center;
    justify-content: center;
    backdrop-filter: blur(5px);
}
.year-modal-content {
    width: 90%;
    max-width: 400px;
    max-height: 80vh;
    background: var(--bg-card);
    border: 1px solid var(--accent-gold);
    border-radius: 12px;
    padding: 20px;
    display: flex;
    flex-direction: column;
    position: relative;
}
.close-btn {
    position: absolute;
    top: 10px;
    right: 15px;
    font-size: 24px;
    background: none;
    border: none;
    color: var(--text-muted);
    cursor: pointer;
}
.modal-title {
    font-size: 18px;
    color: var(--accent-gold);
    margin-bottom: 16px;
    text-align: center;
    font-weight: bold;
}
.modal-body {
    overflow-y: auto;
    font-size: 14px;
    line-height: 1.6;
    padding: 16px;
    color: var(--text-primary);
}
.loading-box {
    padding: 40px;
    text-align: center;
    color: var(--text-muted);
}
.loading-spinner {
    width: 30px;
    height: 30px;
    border: 2px solid rgba(255,255,255,0.1);
    border-top-color: var(--accent-gold);
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin: 0 auto 16px;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* 动画 */
.fade-in-up {
    animation: fadeInUp 0.6s ease-out;
}
</style>
