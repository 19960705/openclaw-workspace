// 情绪类型
export type Mood = 'happy' | 'okay' | 'tired' | 'crashed';

// 效率类型
export type Efficiency = 'high' | 'medium' | 'low';

// 每日打卡记录
export interface DailyLog {
  date: string;           // 格式: 2026-02-15
  mood: Mood;
  energy: 1 | 2 | 3 | 4;  // 🔋 数量 (1-4)
  efficiency: Efficiency;
  createdAt: number;      // Unix timestamp
}

// 周报总结
export interface WeekSummary {
  weekNumber: number;
  year: number;
  startDate: string;
  endDate: string;
  moodDistribution: Record<Mood, number>;
  avgEnergy: number;
  efficiencyTrend: 'up' | 'down' | 'stable';
  avgEfficiency: number;
  insights: string[];
}

// 月历视图的某一天数据
export interface CalendarDay {
  date: string;
  hasLog: boolean;
  log?: DailyLog;
}

// 洞察数据
export interface Insight {
  id: string;
  text: string;
  type: 'positive' | 'neutral' | 'negative';
}
