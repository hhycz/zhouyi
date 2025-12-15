<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue';
import MessageBubble from './MessageBubble.vue';
import TypeWriter from './TypeWriter.vue';
import IntentSelector from '../widgets/IntentSelector.vue';
import BirthDateForm from '../widgets/BirthDateForm.vue';
import LocationPicker from '../widgets/LocationPicker.vue';
import CoinToss from '../widgets/CoinToss.vue';
import BreathGuide from '../widgets/BreathGuide.vue';
import BaziChart from '../results/BaziChart.vue';
import LiuyaoChart from '../results/LiuyaoChart.vue';
import { api } from '@/api';
import type { ChatMessage, DivinationState, BaziRequest, IntentType } from '@/types';

const messages = ref<ChatMessage[]>([]);
const messagesContainer = ref<HTMLElement | null>(null);
const isLoading = ref(false);

// 扩展状态以支持六爻
interface ExtendedState extends DivinationState {
  divinationType: 'bazi' | 'liuyao' | null;
  liuyaoQuestion: string;
  liuyaoResult: any;
}

const state = ref<ExtendedState>({
  step: 'greeting',
  intent: null,
  birthInfo: null,
  location: null,
  result: null,
  divinationType: null,
  liuyaoQuestion: '',
  liuyaoResult: null
});

// 添加系统消息
function addSystemMessage(content: string, widget?: ChatMessage['widget'], data?: any) {
  messages.value.push({
    id: `msg-${Date.now()}`,
    role: 'system',
    content,
    timestamp: Date.now(),
    widget,
    data
  });
  scrollToBottom();
}

// 添加用户消息
function addUserMessage(content: string) {
  messages.value.push({
    id: `msg-${Date.now()}`,
    role: 'user',
    content,
    timestamp: Date.now()
  });
  scrollToBottom();
}

// 滚动到底部
async function scrollToBottom() {
  await nextTick();
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
  }
}

// 开场白
function startGreeting() {
  setTimeout(() => {
    addSystemMessage('万物皆有数，天机可推演。');
  }, 500);
  
  setTimeout(() => {
    addSystemMessage('施主，你为何事而来？', 'intent-selector');
  }, 2000);
}

// 用户选择问卦意图
function handleIntentSelect(intent: IntentType) {
  const intentLabels: Record<IntentType, string> = {
    career: '问前程',
    love: '问姻缘',
    fortune: '问吉凶'
  };
  
  addUserMessage(intentLabels[intent]);
  state.value.intent = intent;
  state.value.liuyaoQuestion = intentLabels[intent];
  
  // 询问使用哪种方式
  setTimeout(() => {
    addSystemMessage('施主想用何法问卦？', 'method-selector');
    state.value.step = 'select-method';
  }, 800);
}

// 选择占卜方式
function handleMethodSelect(method: 'bazi' | 'liuyao') {
  state.value.divinationType = method;
  
  if (method === 'bazi') {
    addUserMessage('八字排盘');
    state.value.step = 'collect-birth';
    setTimeout(() => {
      addSystemMessage('既问此事，当以诚心为引。请告诉我你的生辰，以定乾坤。', 'birth-date-form');
    }, 800);
  } else {
    addUserMessage('六爻金钱卦');
    state.value.step = 'liuyao-calm';
    setTimeout(() => {
      addSystemMessage('起卦前需静心凝神。请随引导调整呼吸，心诚则灵。', 'breath-guide');
    }, 800);
  }
}

// 净心完成后开始抛币
function handleBreathComplete() {
  state.value.step = 'liuyao-toss';
  setTimeout(() => {
    addSystemMessage('气息已定。请心中默念所问之事，摇动铜钱六次。', 'coin-toss');
  }, 500);
}

// 用户提交生辰信息
function handleBirthSubmit(info: {
  year: number;
  month: number;
  day: number;
  hour: number;
  minute: number;
  gender: 0 | 1;
}) {
  const genderText = info.gender === 1 ? '男' : '女';
  addUserMessage(`${genderText}命，${info.year}年${info.month}月${info.day}日 ${info.hour}:${String(info.minute).padStart(2, '0')}`);
  state.value.birthInfo = info;
  state.value.step = 'collect-location';
  
  setTimeout(() => {
    addSystemMessage('排八字需定真太阳时，因各地日出时间不同。请问施主出生在哪座城市？', 'location-picker');
  }, 800);
}

// 用户选择出生地
async function handleLocationSelect(location: { city: string; longitude: number; latitude: number }) {
  addUserMessage(location.city);
  state.value.location = location;
  state.value.step = 'ritual';
  
  setTimeout(() => {
    addSystemMessage(`📍 ${location.city} (东经${location.longitude.toFixed(1)}°)`);
  }, 500);
  
  setTimeout(() => {
    addSystemMessage('气场已定，正在为施主排盘推演...');
    performBaziDivination();
  }, 1500);
}

// 六爻起卦完成
async function handleCoinTossComplete(results: number[]) {
  addUserMessage(`起卦完成: ${results.join(', ')}`);
  state.value.step = 'liuyao-result';
  
  setTimeout(() => {
    addSystemMessage('六爻已成，正在解卦...');
  }, 500);
  
  isLoading.value = true;
  
  try {
    const result = await api.getLiuyaoChart(state.value.liuyaoQuestion, results);
    
    state.value.liuyaoResult = result;
    
    setTimeout(() => {
      addSystemMessage('卦象已成，请看：', 'liuyao-chart', result);
    }, 1000);
    
  } catch (error) {
    console.error('Liuyao error:', error);
    addSystemMessage('解卦过程遇阻，请稍后再试...');
  } finally {
    isLoading.value = false;
  }
}

// 执行八字排盘
async function performBaziDivination() {
  if (!state.value.birthInfo || !state.value.location) return;
  
  isLoading.value = true;
  
  try {
    const request: BaziRequest = {
      birth_year: state.value.birthInfo.year,
      birth_month: state.value.birthInfo.month,
      birth_day: state.value.birthInfo.day,
      birth_hour: state.value.birthInfo.hour,
      birth_minute: state.value.birthInfo.minute,
      longitude: state.value.location.longitude,
      latitude: state.value.location.latitude,
      gender: state.value.birthInfo.gender,
      use_true_solar_time: true
    };
    
    const result = await api.getBaziChart(request);
    state.value.result = result;
    state.value.step = 'result';
    
    if (result.birth_info.solar_correction) {
      const correction = result.birth_info.solar_correction;
      const correctionText = correction.total_correction_minutes >= 0 
        ? `+${correction.total_correction_minutes.toFixed(0)}分钟`
        : `${correction.total_correction_minutes.toFixed(0)}分钟`;
      
      setTimeout(() => {
        addSystemMessage(`⏱️ 真太阳时校正：${correctionText}`);
      }, 500);
    }
    
    setTimeout(() => {
      addSystemMessage('施主命盘已成，且看八字格局：', 'bazi-chart', result);
    }, 1200);
    
  } catch (error) {
    console.error('Divination error:', error);
    addSystemMessage('推演过程遇阻，请稍后再试...');
  } finally {
    isLoading.value = false;
  }
}

onMounted(() => {
  startGreeting();
});
</script>

<template>
  <div class="chat-container">
    <!-- 水墨背景 -->
    <div class="ink-bg"></div>
    
    <!-- 消息列表 -->
    <div ref="messagesContainer" class="messages-area">
      <TransitionGroup name="message">
        <div 
          v-for="msg in messages" 
          :key="msg.id"
          class="message-wrapper"
          :class="msg.role"
        >
          <!-- 文本消息 -->
          <MessageBubble v-if="!msg.widget" :role="msg.role as 'system' | 'user'">
            <TypeWriter :text="msg.content" :delay="30" />
          </MessageBubble>
          
          <!-- 带Widget的消息 -->
          <div v-else class="widget-message">
            <MessageBubble :role="msg.role as 'system' | 'user'">
              <TypeWriter :text="msg.content" :delay="30" />
            </MessageBubble>
            
            <!-- Intent Selector -->
            <IntentSelector 
              v-if="msg.widget === 'intent-selector' && state.step === 'greeting'"
              @select="handleIntentSelect"
            />
            
            <!-- Method Selector -->
            <div v-if="msg.widget === 'method-selector' && state.step === 'select-method'" class="method-selector">
              <button class="method-card" @click="handleMethodSelect('bazi')">
                <span class="icon">📜</span>
                <span class="label">八字排盘</span>
                <span class="desc">需提供生辰八字</span>
              </button>
              <button class="method-card" @click="handleMethodSelect('liuyao')">
                <span class="icon">🪙</span>
                <span class="label">六爻金钱卦</span>
                <span class="desc">摇卦起卦，即时问事</span>
              </button>
            </div>
            
            <!-- Birth Date Form -->
            <BirthDateForm 
              v-if="msg.widget === 'birth-date-form' && state.step === 'collect-birth'"
              @submit="handleBirthSubmit"
            />
            
            <!-- Location Picker -->
            <LocationPicker 
              v-if="msg.widget === 'location-picker' && state.step === 'collect-location'"
              @select="handleLocationSelect"
            />
            
            <!-- Breath Guide -->
            <BreathGuide 
              v-if="msg.widget === 'breath-guide' && state.step === 'liuyao-calm'"
              @complete="handleBreathComplete"
            />
            
            <!-- Coin Toss -->
            <CoinToss 
              v-if="msg.widget === 'coin-toss' && state.step === 'liuyao-toss'"
              @complete="handleCoinTossComplete"
            />
            
            <!-- Bazi Chart -->
            <BaziChart 
              v-if="msg.widget === 'bazi-chart' && msg.data"
              :data="msg.data"
            />
            
            <!-- Liuyao Chart -->
            <LiuyaoChart 
              v-if="msg.widget === 'liuyao-chart' && msg.data"
              :data="msg.data"
            />
          </div>
        </div>
      </TransitionGroup>
      
      <!-- Loading -->
      <div v-if="isLoading" class="loading-indicator">
        <div class="loading-dots">
          <span></span>
          <span></span>
          <span></span>
        </div>
      </div>
    </div>
    
    <!-- 标题区域 -->
    <div class="header">
      <h1>周易卜卦</h1>
      <p>智能排盘 · 命理推演</p>
    </div>
  </div>
</template>

<style scoped>
.chat-container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
  z-index: 1;
}

.header {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  padding: 24px 20px;
  text-align: center;
  background: linear-gradient(to bottom, 
    rgba(10, 10, 15, 0.95) 0%,
    rgba(10, 10, 15, 0.8) 50%,
    transparent 100%);
  z-index: 10;
  backdrop-filter: blur(10px);
}

.header h1 {
  font-size: 32px;
  font-weight: 300;
  color: var(--accent-gold);
  letter-spacing: 12px;
  margin-bottom: 8px;
  text-shadow: 0 0 20px rgba(212, 175, 55, 0.5);
}

.header p {
  font-size: 14px;
  color: var(--text-secondary);
  letter-spacing: 6px;
  opacity: 0.8;
}

.messages-area {
  flex: 1;
  overflow-y: auto;
  padding: 120px 20px 40px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  background: radial-gradient(ellipse at center, transparent 0%, rgba(0, 0, 0, 0.3) 100%);
}

.message-wrapper {
  display: flex;
  flex-direction: column;
  max-width: 85%;
}

.message-wrapper.system {
  align-self: flex-start;
}

.message-wrapper.user {
  align-self: flex-end;
}

.widget-message {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* Method Selector */
.method-selector {
  display: flex;
  gap: 12px;
  margin-top: 8px;
}

.method-card {
  flex: 1;
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

.method-card:hover {
  border-color: var(--accent-gold);
  transform: translateY(-4px);
  box-shadow: var(--shadow-glow);
}

.method-card .icon {
  font-size: 32px;
}

.method-card .label {
  font-size: 16px;
  color: var(--accent-gold);
  font-weight: 500;
}

.method-card .desc {
  font-size: 12px;
  color: var(--text-secondary);
}

/* Message transitions */
.message-enter-active {
  animation: fadeInUp 0.4s ease-out;
}

.message-leave-active {
  animation: fadeIn 0.2s ease-out reverse;
}

/* Loading indicator */
.loading-indicator {
  display: flex;
  justify-content: flex-start;
  padding: 10px;
}

.loading-dots {
  display: flex;
  gap: 6px;
}

.loading-dots span {
  width: 8px;
  height: 8px;
  background: var(--accent-gold);
  border-radius: 50%;
  animation: pulse 1.4s infinite ease-in-out both;
}

.loading-dots span:nth-child(1) { animation-delay: -0.32s; }
.loading-dots span:nth-child(2) { animation-delay: -0.16s; }
.loading-dots span:nth-child(3) { animation-delay: 0s; }
</style>
