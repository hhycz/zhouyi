/**
 * API client for Zhou Yi Divination backend
 */
import axios from 'axios';
import type { BaziRequest, BaziResponse } from '@/types';

// 动态获取后端地址，支持局域网访问
const API_HOST = window.location.hostname;
const API_BASE = `http://${API_HOST}:8000/api`;

export const api = {
    /**
     * 八字排盘
     */
    async getBaziChart(request: BaziRequest): Promise<BaziResponse> {
        const response = await axios.post<BaziResponse>(
            `${API_BASE}/divination/bazi`,
            request
        );
        return response.data;
    },

    /**
     * 八字 AI 解读
     */
    async getBaziAIInterpretation(request: BaziRequest) {
        const response = await axios.post(`${API_BASE}/divination/bazi/ai`, request);
        return response.data;
    },

    /**
     * 八字流年分析
     */
    async analyzeBaziYear(request: BaziRequest, year: number): Promise<{ success: boolean; content: string }> {
        const response = await axios.post(`${API_BASE}/divination/bazi/analyze-year`, request, {
            params: { year }
        });
        return response.data;
    },

    /**
     * 六爻起卦
     */
    async getLiuyaoChart(question: string, coinResults: number[]) {
        const response = await axios.post(`${API_BASE}/divination/liuyao`, {
            question,
            coin_results: coinResults
        });
        return response.data;
    },

    /**
     * AI 解卦
     */
    async getAIInterpretation(params: {
        question: string;
        hexagramName: string;
        changedHexagramName?: string;
        movingPositions?: number[];
        interpretationData?: any;
    }) {
        const response = await axios.post(`${API_BASE}/divination/liuyao/ai-interpret`, {
            question: params.question,
            hexagram_name: params.hexagramName,
            changed_hexagram_name: params.changedHexagramName,
            moving_positions: params.movingPositions,
            interpretation_data: params.interpretationData
        });
        return response.data;
    },

    /**
     * 公历转农历
     */
    async solarToLunar(year: number, month: number, day: number) {
        const response = await axios.post(`${API_BASE}/calendar/convert`, {
            year,
            month,
            day,
            source_type: 'solar'
        });
        return response.data;
    },

    /**
     * 获取今日信息
     */
    async getTodayInfo() {
        const response = await axios.get(`${API_BASE}/calendar/today`);
        return response.data;
    },

    /**
     * 计算真太阳时
     */
    async getTrueSolarTime(
        year: number,
        month: number,
        day: number,
        hour: number,
        minute: number,
        longitude: number
    ) {
        const response = await axios.post(`${API_BASE}/calendar/true-solar-time`, {
            year,
            month,
            day,
            hour,
            minute,
            longitude
        });
        return response.data;
    }
};

