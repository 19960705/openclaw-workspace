import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { WeekSummary } from '../../types';
import { COLORS, EFFICIENCY_EMOJIS } from '../../constants';

interface WeekSummaryCardProps {
  summary: WeekSummary;
  onPress?: () => void;
}

export const WeekSummaryCard: React.FC<WeekSummaryCardProps> = ({
  summary,
  onPress,
}) => {
  const { moodDistribution, avgEfficiency, avgEnergy, insights } = summary;

  // 计算状态不错的天数
  const goodDays = moodDistribution.happy + moodDistribution.okay;
  const totalLogged = Object.values(moodDistribution).reduce((a, b) => a + b, 0);

  return (
    <TouchableOpacity style={styles.card} onPress={onPress} activeOpacity={0.7}>
      <View style={styles.header}>
        <Text style={styles.title}>第 {summary.weekNumber} 周</Text>
        <Text style={styles.dateRange}>
          {summary.startDate} - {summary.endDate}
        </Text>
      </View>

      <View style={styles.statsRow}>
        <View style={styles.statItem}>
          <Text style={styles.statEmoji}>
            {goodDays >= totalLogged * 0.7 ? '🌟' : '📊'}
          </Text>
          <Text style={styles.statLabel}>状态不错</Text>
          <Text style={styles.statValue}>{goodDays} 天</Text>
        </View>

        <View style={styles.statItem}>
          <Text style={styles.statEmoji}>⚡</Text>
          <Text style={styles.statLabel}>平均效率</Text>
          <Text style={styles.statValue}>{avgEfficiency}%</Text>
        </View>

        <View style={styles.statItem}>
          <Text style={styles.statEmoji}>🔋</Text>
          <Text style={styles.statLabel}>平均精力</Text>
          <Text style={styles.statValue}>{avgEnergy.toFixed(1)}</Text>
        </View>
      </View>

      {insights.length > 0 && (
        <View style={styles.insightRow}>
          <Text style={styles.insightLabel}>💡 {insights[0]}</Text>
        </View>
      )}

      <View style={styles.footer}>
        <Text style={styles.footerText}>查看完整周报 →</Text>
      </View>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  card: {
    backgroundColor: COLORS.card,
    borderRadius: 16,
    padding: 20,
    marginHorizontal: 20,
    marginBottom: 16,
    shadowColor: COLORS.shadow,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 1,
    shadowRadius: 12,
    elevation: 3,
  },
  header: {
    marginBottom: 16,
  },
  title: {
    fontSize: 20,
    fontWeight: '700',
    color: COLORS.text,
    marginBottom: 4,
  },
  dateRange: {
    fontSize: 14,
    color: COLORS.textSecondary,
  },
  statsRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 16,
  },
  statItem: {
    alignItems: 'center',
    flex: 1,
  },
  statEmoji: {
    fontSize: 24,
    marginBottom: 8,
  },
  statLabel: {
    fontSize: 12,
    color: COLORS.textSecondary,
    marginBottom: 4,
  },
  statValue: {
    fontSize: 18,
    fontWeight: '600',
    color: COLORS.text,
  },
  insightRow: {
    backgroundColor: COLORS.background,
    borderRadius: 12,
    padding: 12,
    marginBottom: 16,
  },
  insightLabel: {
    fontSize: 14,
    color: COLORS.text,
  },
  footer: {
    borderTopWidth: 1,
    borderTopColor: COLORS.border,
    paddingTop: 12,
    alignItems: 'center',
  },
  footerText: {
    fontSize: 14,
    fontWeight: '600',
    color: COLORS.happy,
  },
});
