import React, { useState, useMemo } from 'react';
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
import { MonthlyCalendarScreenProps } from '../../types/navigation';
import { COLORS, MOOD_EMOJIS, EFFICIENCY_EMOJIS } from '../constants';
import { getAllLogs } from '../utils/storage';
import { DailyLog, Mood, Efficiency } from '../types';
import dayjs from 'dayjs';

type ParamList = {
  MonthlyCalendar: { year: number; month: number };
};

const { width } = Dimensions.get('window');
const DAYS_IN_WEEK = 7;

export const MonthlyCalendarScreen: React.FC<MonthlyCalendarScreenProps> = ({
  navigation,
}) => {
  const route = useRoute<RouteProp<ParamList, 'MonthlyCalendar'>>();
  const initialYear = route.params?.year || dayjs().year();
  const initialMonth = route.params?.month || dayjs().month() + 1;

  const [currentDate, setCurrentDate] = useState(
    dayjs().year(initialYear).month(initialMonth - 1)
  );
  const [logs, setLogs] = useState<Map<string, DailyLog>>(new Map());

  // 加载数据
  React.useEffect(() => {
    const allLogs = getAllLogs();
    const logsMap = new Map<string, DailyLog>();
    allLogs.forEach(log => logsMap.set(log.date, log));
    setLogs(logsMap);
  }, []);

  const year = currentDate.year();
  const month = currentDate.month();

  // 获取月份天数
  const daysInMonth = currentDate.daysInMonth();
  const firstDayOfMonth = currentDate.startOf('month').day();

  // 生成日历网格
  const calendarDays = useMemo(() => {
    const days: (dayjs.Dayjs | null)[] = [];

    // 填充月初空白
    for (let i = 0; i < firstDayOfMonth; i++) {
      days.push(null);
    }

    // 填充日期
    for (let i = 1; i <= daysInMonth; i++) {
      days.push(currentDate.date(i));
    }

    return days;
  }, [currentDate, daysInMonth, firstDayOfMonth]);

  // 周几标题
  const weekDays = ['日', '一', '二', '三', '四', '五', '六'];

  const getMoodColor = (mood: Mood): string => {
    const colors: Record<Mood, string> = {
      happy: COLORS.happy,
      okay: COLORS.okay,
      tired: COLORS.tired,
      crashed: COLORS.crashed,
    };
    return colors[mood];
  };

  const getEfficiencyColor = (efficiency: Efficiency): string => {
    const colors: Record<Efficiency, string> = {
      high: COLORS.high,
      medium: COLORS.medium,
      low: COLORS.low,
    };
    return colors[efficiency];
  };

  const dayWidth = (width - 40) / 7;

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.goBack()} style={styles.backButton}>
          <Text style={styles.backText}>← 返回</Text>
        </TouchableOpacity>
        <Text style={styles.title}>{year} 年 {month + 1} 月</Text>
        <View style={styles.headerRight} />
      </View>

      <ScrollView style={styles.scrollView}>
        {/* Month Navigation */}
        <View style={styles.monthNav}>
          <TouchableOpacity
            onPress={() => setCurrentDate(currentDate.subtract(1, 'month'))}
          >
            <Text style={styles.navArrow}>← 上月</Text>
          </TouchableOpacity>
          <Text style={styles.monthText}>{currentDate.format('YYYY 年 M 月')}</Text>
          <TouchableOpacity
            onPress={() => setCurrentDate(currentDate.add(1, 'month'))}
          >
            <Text style={styles.navArrow}>下月 →</Text>
          </TouchableOpacity>
        </View>

        {/* Week Days Header */}
        <View style={styles.weekHeader}>
          {weekDays.map(day => (
            <Text key={day} style={styles.weekDayText}>{day}</Text>
          ))}
        </View>

        {/* Calendar Grid */}
        <View style={styles.calendarGrid}>
          {calendarDays.map((day, index) => {
            if (!day) {
              return <View key={`empty-${index}`} style={[styles.dayCell, { width: dayWidth }]} />;
            }

            const dateStr = day.format('YYYY-MM-DD');
            const log = logs.get(dateStr);
            const isToday = dateStr === dayjs().format('YYYY-MM-DD');

            return (
              <TouchableOpacity
                key={dateStr}
                style={[
                  styles.dayCell,
                  { width: dayWidth },
                  isToday && styles.todayCell,
                ]}
                onPress={() => {
                  if (log) {
                    // 显示详情弹窗
                  }
                }}
              >
                <Text style={[styles.dayText, isToday && styles.todayText]}>
                  {day.format('D')}
                </Text>

                {log && (
                  <View style={styles.dayIcons}>
                    <Text style={styles.moodEmoji}>{MOOD_EMOJIS[log.mood]}</Text>
                    <View
                      style={[
                        styles.efficiencyDot,
                        { backgroundColor: getEfficiencyColor(log.efficiency) },
                      ]}
                    />
                  </View>
                )}
              </TouchableOpacity>
            );
          })}
        </View>

        {/* Legend */}
        <View style={styles.legend}>
          <View style={styles.legendItem}>
            <Text style={styles.legendEmoji}>😊</Text>
            <Text style={styles.legendLabel}>开心</Text>
          </View>
          <View style={styles.legendItem}>
            <Text style={styles.legendEmoji}>😐</Text>
            <Text style={styles.legendLabel}>一般</Text>
          </View>
          <View style={styles.legendItem}>
            <Text style={styles.legendEmoji}>😫</Text>
            <Text style={styles.legendLabel}>疲惫</Text>
          </View>
          <View style={styles.legendItem}>
            <Text style={styles.legendEmoji}>🤯</Text>
            <Text style={styles.legendLabel}>崩溃</Text>
          </View>
        </View>

        {/* Stats Summary */}
        <View style={styles.statsSection}>
          <Text style={styles.sectionTitle}>📊 本月统计</Text>
          <View style={styles.statsRow}>
            <View style={styles.statCard}>
              <Text style={styles.statValue}>
                {Array.from(logs.values()).filter(l => l.date.startsWith(currentDate.format('YYYY-MM'))).length}
              </Text>
              <Text style={styles.statLabel}>打卡天数</Text>
            </View>
            <View style={styles.statCard}>
              <Text style={styles.statValue}>
                {Array.from(logs.values()).filter(l => l.date.startsWith(currentDate.format('YYYY-MM'))).length > 0 ? '—' : '0'}
              </Text>
              <Text style={styles.statLabel}>记录天数</Text>
            </View>
          </View>
        </View>

        <View style={styles.bottomSpacer} />
      </ScrollView>
    </View>
  );
};

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
  monthNav: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 20,
    marginBottom: 16,
  },
  navArrow: {
    fontSize: 14,
    color: COLORS.textSecondary,
    padding: 8,
  },
  monthText: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.text,
  },
  weekHeader: {
    flexDirection: 'row',
    paddingHorizontal: 10,
    marginBottom: 8,
  },
  weekDayText: {
    width: (width - 40) / 7,
    textAlign: 'center',
    fontSize: 12,
    color: COLORS.textSecondary,
    fontWeight: '500',
  },
  calendarGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    paddingHorizontal: 10,
  },
  dayCell: {
    height: 60,
    alignItems: 'center',
    justifyContent: 'center',
    borderRadius: 8,
    marginHorizontal: 2,
    marginVertical: 2,
  },
  todayCell: {
    backgroundColor: COLORS.background,
    borderWidth: 1,
    borderColor: COLORS.border,
  },
  dayText: {
    fontSize: 14,
    color: COLORS.text,
    marginBottom: 2,
  },
  todayText: {
    fontWeight: '700',
    color: COLORS.text,
  },
  dayIcons: {
    alignItems: 'center',
    gap: 2,
  },
  moodEmoji: {
    fontSize: 14,
  },
  efficiencyDot: {
    width: 6,
    height: 6,
    borderRadius: 3,
  },
  legend: {
    flexDirection: 'row',
    justifyContent: 'center',
    gap: 20,
    paddingVertical: 16,
  },
  legendItem: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  legendEmoji: {
    fontSize: 14,
    marginRight: 4,
  },
  legendLabel: {
    fontSize: 12,
    color: COLORS.textSecondary,
  },
  statsSection: {
    paddingHorizontal: 20,
    marginTop: 16,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.text,
    marginBottom: 12,
  },
  statsRow: {
    flexDirection: 'row',
    gap: 12,
  },
  statCard: {
    flex: 1,
    backgroundColor: COLORS.card,
    borderRadius: 12,
    padding: 16,
    alignItems: 'center',
  },
  statValue: {
    fontSize: 24,
    fontWeight: '700',
    color: COLORS.text,
    marginBottom: 4,
  },
  statLabel: {
    fontSize: 12,
    color: COLORS.textSecondary,
  },
  bottomSpacer: {
    height: 40,
  },
});
