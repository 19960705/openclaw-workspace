import dayjs from 'dayjs';
import { DailyLog, WeekSummary, Mood, Efficiency, Insight } from '../types';
import { getLogsByWeek, getLogsByMonth } from './storage';
import weekOfYear from 'dayjs/plugin/weekOfYear';
import isoWeek from 'dayjs/plugin/isoWeek';

dayjs.extend(weekOfYear);
dayjs.extend(isoWeek);

// 计算情绪分布
const calculateMoodDistribution = (logs: DailyLog[]): Record<Mood, number> => {
  const distribution: Record<Mood, number> = {
    happy: 0,
    okay: 0,
    tired: 0,
    crashed: 0,
  };

  logs.forEach(log => {
    distribution[log.mood]++;
  });

  return distribution;
};

// 计算平均精力
const calculateAvgEnergy = (logs: DailyLog[]): number => {
  if (logs.length === 0) return 0;
  const total = logs.reduce((sum, log) => sum + log.energy, 0);
  return Math.round((total / logs.length) * 10) / 10;
};

// 计算平均效率
const calculateAvgEfficiency = (logs: DailyLog[]): number => {
  if (logs.length === 0) return 0;
  const scoreMap = { high: 100, medium: 65, low: 35 };
  const total = logs.reduce((sum, log) => sum + scoreMap[log.efficiency], 0);
  return Math.round(total / logs.length);
};

// 生成洞察
const generateInsights = (
  logs: DailyLog[],
  weekNumber: number,
  year: number
): string[] => {
  const insights: string[] = [];

  if (logs.length === 0) return ['还没有打卡数据'];

  // 情绪洞察
  const moodDist = calculateMoodDistribution(logs);
  const goodDays = moodDist.happy + moodDist.okay;
  const totalDays = logs.length;

  if (goodDays >= totalDays * 0.8) {
    insights.push(`这周你有 ${goodDays} 天状态不错 🌟`);
  } else if (goodDays >= totalDays * 0.5) {
    insights.push(`这周你有 ${goodDays} 天状态还可以`);
  }

  // 效率洞察
  const avgEff = calculateAvgEfficiency(logs);
  if (avgEff >= 80) {
    insights.push('整体效率不错，继续保持 💪');
  } else if (avgEff < 50) {
    insights.push('这周效率偏低，对自己温柔一点');
  }

  // 对比上周
  const prevWeek = weekNumber === 1 ? 52 : weekNumber - 1;
  const prevYear = weekNumber === 1 ? year - 1 : year;
  const prevLogs = getLogsByWeek(prevYear, prevWeek);

  if (prevLogs.length > 0) {
    const prevAvg = calculateAvgEfficiency(prevLogs);
    const diff = avgEff - prevAvg;
    if (diff > 10) {
      insights.push('这周效率比上周提升了 10%+ 📈');
    } else if (diff < -10) {
      insights.push('这周效率比上周略低，没关系的');
    }
  }

  // 精力洞察
  const avgEnergy = calculateAvgEnergy(logs);
  if (avgEnergy >= 3) {
    insights.push('精力充沛，保持这个节奏');
  } else if (avgEnergy < 2) {
    insights.push('这周有点累，记得多休息');
  }

  return insights.slice(0, 4); // 最多 4 条
};

// 获取效率趋势
const getEfficiencyTrend = (
  logs: DailyLog[]
): 'up' | 'down' | 'stable' => {
  if (logs.length < 3) return 'stable';

  const sorted = [...logs].sort((a, b) =>
    dayjs(a.date).unix() - dayjs(b.date).unix()
  );

  const firstHalf = sorted.slice(0, Math.floor(sorted.length / 2));
  const secondHalf = sorted.slice(Math.floor(sorted.length / 2));

  const firstAvg = calculateAvgEfficiency(firstHalf);
  const secondAvg = calculateAvgEfficiency(secondHalf);

  if (secondAvg - firstAvg > 10) return 'up';
  if (firstAvg - secondAvg > 10) return 'down';
  return 'stable';
};

// 生成周报
export const generateWeekSummary = (
  year: number,
  weekNumber: number
): WeekSummary => {
  const logs = getLogsByWeek(year, weekNumber);

  // 计算日期范围
  const startOfWeek = dayjs().year(year).isoWeek(weekNumber).startOf('isoWeek');
  const endOfWeek = dayjs().year(year).isoWeek(weekNumber).endOf('isoWeek');

  return {
    weekNumber,
    year,
    startDate: startOfWeek.format('YYYY-MM-DD'),
    endDate: endOfWeek.format('YYYY-MM-DD'),
    moodDistribution: calculateMoodDistribution(logs),
    avgEnergy: calculateAvgEnergy(logs),
    efficiencyTrend: getEfficiencyTrend(logs),
    avgEfficiency: calculateAvgEfficiency(logs),
    insights: generateInsights(logs, weekNumber, year),
  };
};

// 生成日洞察
export const generateDailyInsight = (log: DailyLog): string => {
  const energyEfficiency = {
    high: { high: '效率爆表的一天', medium: '稳步前进', low: '有点反差' },
    medium: { high: '精力充沛', medium: '平稳的一天', low: '给自己放个假吧' },
    low: { high: '硬撑辛苦了', medium: '有点累', low: '崩溃日，抱抱自己' },
  };

  return energyEfficiency[log.efficiency][log.efficiency];
};

// 生成洞察列表
export const getInsights = (): Insight[] => {
  const today = dayjs();
  const currentWeekLogs = getLogsByWeek(today.year(), today.isoWeek());

  if (currentWeekLogs.length === 0) {
    return [
      {
        id: '1',
        text: '开始记录，了解自己的节奏',
        type: 'positive',
      },
    ];
  }

  const summary = generateWeekSummary(today.year(), today.isoWeek());

  return summary.insights.map((text, index) => ({
    id: String(index),
    text,
    type: text.includes('提升') || text.includes('不错') ? 'positive' :
          text.includes('偏低') || text.includes('累') ? 'negative' : 'neutral',
  }));
};
