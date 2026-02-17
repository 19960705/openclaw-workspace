import React, { useMemo } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Dimensions,
} from 'react-native';
import { RouteProp, useRoute } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { WeeklyReportScreenProps } from '../../types/navigation';
import { COLORS, MOOD_EMOJIS, MOOD_LABELS, EFFICIENCY_EMOJIS } from '../constants';
import { generateWeekSummary, getLogsByWeek } from '../utils/insights';
import { DailyLog } from '../types';

type ParamList = {
  WeeklyReport: { year: number; weekNumber: number };
};

// 图表尺寸
const CHART_SIZE = 160;

export const WeeklyReportScreen: React.FC<WeeklyReportScreenProps> = ({
  navigation,
}) => {
  const route = useRoute<RouteProp<ParamList, 'WeeklyReport'>>();
  const { year, weekNumber } = route.params;

  const summary = useMemo(() => {
    return generateWeekSummary(year, weekNumber);
  }, [year, weekNumber]);

  const logs = useMemo(() => {
    return getLogsByWeek(year, weekNumber);
  }, [year, weekNumber]);

  // 情绪分布数据
  const moodData = useMemo(() => {
    return Object.entries(summary.moodDistribution).map(([mood, count]) => ({
      mood,
      count,
      percentage: logs.length > 0 ? Math.round((count / logs.length) * 100) : 0,
    }));
  }, [summary, logs]);

  // 渲染简单圆环图
  const renderMoodChart = () => {
    const colors = {
      happy: COLORS.happy,
      okay: COLORS.okay,
      tired: COLORS.tired,
      crashed: COLORS.crashed,
    };

    const total = logs.length || 1;
    const segments = Object.entries(summary.moodDistribution).filter(
      ([, count]) => count > 0
    );

    return (
      <View style={styles.chartContainer}>
        <View style={styles.chart}>
          {segments.map(([mood, count], index) => {
            const prevPercent = segments
              .slice(0, index)
              .reduce((sum, [, c]) => sum + (c / total) * 360, 0);
            const percent = (count / total) * 360;
            const color = colors[mood as keyof typeof colors];

            return (
              <View
                key={mood}
                style={[
                  styles.chartSegment,
                  {
                    backgroundColor: color,
                    transform: [{ rotate: `${prevPercent}deg` }],
                  },
                ]}
              />
            );
          })}
          <View style={styles.chartCenter}>
            <Text style={styles.chartCenterEmoji}>
              {MOOD_EMOJIS[summary.moodDistribution.happy >= summary.moodDistribution.okay ? 'happy' : 'okay']}
            </Text>
          </View>
        </View>

        {/* Legend */}
        <View style={styles.chartLegend}>
          {moodData.map(({ mood, percentage }) => (
            <View key={mood} style={styles.legendItem}>
              <Text style={styles.legendEmoji}>{MOOD_EMOJIS[mood as keyof typeof MOOD_EMOJIS]}</Text>
              <Text style={styles.legendText}>
                {MOOD_LABELS[mood as keyof typeof MOOD_LABELS]} {percentage}%
              </Text>
            </View>
          ))}
        </View>
      </View>
    );
  };

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.goBack()} style={styles.backButton}>
          <Text style={styles.backText}>← 返回</Text>
        </TouchableOpacity>
        <Text style={styles.title}>第 {weekNumber} 周周报</Text>
        <View style={styles.headerRight} />
      </View>

      <ScrollView style={styles.scrollView} showsVerticalScrollIndicator={false}>
        {/* Date Range */}
        <Text style={styles.dateRange}>
          {summary.startDate} - {summary.endDate}
        </Text>

        {/* Mood Chart */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>😌 情绪分布</Text>
          {renderMoodChart()}
        </View>

        {/* Efficiency Stats */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>⚡ 效率统计</Text>
          <View style={styles.efficiencyCard}>
            <View style={styles.efficiencyMain}>
              <Text style={styles.efficiencyLabel}>平均效率</Text>
              <Text style={styles.efficiencyValue}>{summary.avgEfficiency}%</Text>
              <View
                style={[
                  styles.efficiencyTrend,
                  {
                    backgroundColor:
                      summary.efficiencyTrend === 'up'
                        ? COLORS.high
                        : summary.efficiencyTrend === 'down'
                        ? COLORS.low
                        : COLORS.medium,
                  },
                ]}
              >
                <Text style={styles.efficiencyTrendText}>
                  {summary.efficiencyTrend === 'up'
                    ? '📈 上升'
                    : summary.efficiencyTrend === 'down'
                    ? '📉 下降'
                    : '➡️ 稳定'}
                </Text>
              </View>
            </View>

            {/* Daily Efficiency */}
            <View style={styles.dailyEfficiencyRow}>
              {logs.sort((a, b) => a.date.localeCompare(b.date)).map((log) => (
                <View key={log.date} style={styles.dailyEfficiencyItem}>
                  <Text style={styles.dailyEmoji}>{EFFICIENCY_EMOJIS[log.efficiency]}</Text>
                  <Text style={styles.dailyDate}>{dayjs(log.date).format('ddd')}</Text>
                </View>
              ))}
            </View>
          </View>
        </View>

        {/* Energy Stats */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>🔋 精力趋势</Text>
          <View style={styles.energyCard}>
            <Text style={styles.energyLabel}>平均精力</Text>
            <Text style={styles.energyValue}>
              {Array(Math.round(summary.avgEnergy)).fill('🔋').join('')}
            </Text>
            <Text style={styles.energySubtext}>
              {summary.avgEnergy >= 3 ? '精力充沛的一周' :
               summary.avgEnergy >= 2 ? '平稳的一周' : '有点累的一周'}
            </Text>
          </View>
        </View>

        {/* Insights */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>💡 洞察</Text>
          {summary.insights.map((insight, index) => (
            <View key={index} style={styles.insightItem}>
              <Text style={styles.insightText}>{insight}</Text>
            </View>
          ))}
        </View>

        {/* Bottom Spacer */}
        <View style={styles.bottomSpacer} />
      </ScrollView>
    </View>
  );
};

// 导入 dayjs
import dayjs from 'dayjs';

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingTop: 60,
    paddingHorizontal: 20,
    paddingBottom: 16,
  },
  backButton: {
    padding: 8,
  },
  backText: {
    fontSize: 16,
    color: COLORS.textSecondary,
  },
  title: {
    fontSize: 20,
    fontWeight: '700',
    color: COLORS.text,
  },
  headerRight: {
    width: 60,
  },
  scrollView: {
    flex: 1,
  },
  dateRange: {
    textAlign: 'center',
    fontSize: 14,
    color: COLORS.textSecondary,
    marginBottom: 20,
  },
  section: {
    paddingHorizontal: 20,
    marginBottom: 24,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: COLORS.text,
    marginBottom: 16,
  },
  chartContainer: {
    alignItems: 'center',
  },
  chart: {
    width: CHART_SIZE,
    height: CHART_SIZE,
    borderRadius: CHART_SIZE / 2,
    backgroundColor: COLORS.card,
    justifyContent: 'center',
    alignItems: 'center',
    overflow: 'hidden',
  },
  chartSegment: {
    position: 'absolute',
    width: '100%',
    height: '100%',
  },
  chartCenter: {
    width: CHART_SIZE * 0.5,
    height: CHART_SIZE * 0.5,
    borderRadius: CHART_SIZE * 0.25,
    backgroundColor: COLORS.background,
    justifyContent: 'center',
    alignItems: 'center',
  },
  chartCenterEmoji: {
    fontSize: 40,
  },
  chartLegend: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'center',
    marginTop: 16,
    gap: 16,
  },
  legendItem: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  legendEmoji: {
    fontSize: 16,
    marginRight: 6,
  },
  legendText: {
    fontSize: 14,
    color: COLORS.textSecondary,
  },
  efficiencyCard: {
    backgroundColor: COLORS.card,
    borderRadius: 16,
    padding: 20,
  },
  efficiencyMain: {
    alignItems: 'center',
    marginBottom: 16,
  },
  efficiencyLabel: {
    fontSize: 14,
    color: COLORS.textSecondary,
    marginBottom: 4,
  },
  efficiencyValue: {
    fontSize: 48,
    fontWeight: '700',
    color: COLORS.text,
    marginBottom: 8,
  },
  efficiencyTrend: {
    paddingHorizontal: 16,
    paddingVertical: 6,
    borderRadius: 20,
  },
  efficiencyTrendText: {
    fontSize: 14,
    fontWeight: '500',
    color: '#fff',
  },
  dailyEfficiencyRow: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    borderTopWidth: 1,
    borderTopColor: COLORS.border,
    paddingTop: 16,
  },
  dailyEfficiencyItem: {
    alignItems: 'center',
  },
  dailyEmoji: {
    fontSize: 24,
    marginBottom: 4,
  },
  dailyDate: {
    fontSize: 12,
    color: COLORS.textSecondary,
  },
  energyCard: {
    backgroundColor: COLORS.card,
    borderRadius: 16,
    padding: 20,
    alignItems: 'center',
  },
  energyLabel: {
    fontSize: 14,
    color: COLORS.textSecondary,
    marginBottom: 8,
  },
  energyValue: {
    fontSize: 32,
    marginBottom: 8,
  },
  energySubtext: {
    fontSize: 14,
    color: COLORS.textSecondary,
  },
  insightItem: {
    backgroundColor: COLORS.card,
    borderRadius: 12,
    padding: 14,
    marginBottom: 8,
  },
  insightText: {
    fontSize: 14,
    color: COLORS.text,
    lineHeight: 20,
  },
  bottomSpacer: {
    height: 40,
  },
});
