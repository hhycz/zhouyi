/**
 * API types for Zhou Yi Divination System
 */

export interface BaziRequest {
    birth_year: number;
    birth_month: number;
    birth_day: number;
    birth_hour: number;
    birth_minute?: number;
    longitude?: number;
    latitude?: number;
    gender: 0 | 1;
    use_true_solar_time?: boolean;
}

export interface Pillar {
    position: string;
    position_cn: string;
    gan: string;
    zhi: string;
    gan_zhi: string;
    gan_element: string;
    zhi_element: string;
    gan_yinyang: string;
    ten_god: string;
    hidden_stems: string[];
    nayin: string;
}

export interface DayMaster {
    gan: string;
    element: string;
    yinyang: string;
}

export interface SolarCorrection {
    original_time: string;
    true_solar_time: string;
    longitude: number;
    longitude_correction_minutes: number;
    eot_correction_minutes: number;
    total_correction_minutes: number;
}

export interface BirthInfo {
    solar_date: string;
    true_solar_time: string | null;
    lunar_date: string;
    longitude: number;
    latitude: number;
    gender: string;
    solar_correction: SolarCorrection | null;
}

export interface ChartInfo {
    pillars: Pillar[];
    day_master: DayMaster;
    elements_count: Record<string, number>;
}

export interface LiuNian {
    year: number;
    age: number;
    gan_zhi: string;
    ten_god: string;
    events: string[];
}

export interface LuckCycle {
    index: number;
    start_age: number;
    end_age: number;
    start_year: number;
    end_year: number;
    gan_zhi: string;
    years: LiuNian[];
}

export interface AdditionalInfo {
    zodiac: string;
    constellation: string;
    current_jieqi: string | null;
    next_jieqi: string | null;
}

export interface AnalysisDetail {
    score: number;
    level: string;
    level_desc: string;
    details: string[];
    day_element: string;
}

export interface UsefulGods {
    xi_shen: string[];
    yong_shen: string | null;
    ji_shen: string[];
    xian_shen: string[];
    tiao_hou?: string;
    tong_guan?: string;
}

export interface PatternInfo {
    name: string;
    type: string;
    revealed: boolean;
    desc: string;
}

export interface PatternAnalysis {
    main_pattern: PatternInfo | null;
    all_patterns: PatternInfo[];
    strength_level: string;
}

export interface BaziResponse {
    birth_info: BirthInfo;
    chart: ChartInfo;
    luck_cycles: LuckCycle[];
    strength_analysis: AnalysisDetail;
    useful_gods: UsefulGods;
    pattern_analysis: PatternAnalysis;
    additional_info: AdditionalInfo;
}

// Chat UI types
export type MessageRole = 'system' | 'user' | 'widget';

export type IntentType = 'career' | 'love' | 'fortune';

export interface ChatMessage {
    id: string;
    role: MessageRole;
    content: string;
    timestamp: number;
    widget?: WidgetType;
    data?: any;
}

export type WidgetType =
    | 'intent-selector'
    | 'method-selector'
    | 'birth-date-form'
    | 'location-picker'
    | 'breath-guide'
    | 'coin-toss'
    | 'bazi-chart'
    | 'liuyao-chart'
    | 'loading';

export interface DivinationState {
    step: 'greeting' | 'intent' | 'select-method' | 'collect-birth' | 'collect-location' | 'ritual' | 'result' | 'liuyao-calm' | 'liuyao-toss' | 'liuyao-result';
    intent: IntentType | null;
    birthInfo: {
        year: number;
        month: number;
        day: number;
        hour: number;
        minute: number;
        gender: 0 | 1;
    } | null;
    location: {
        city: string;
        longitude: number;
        latitude: number;
    } | null;
    result: BaziResponse | null;
}
