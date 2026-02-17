import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import dayjs from 'dayjs';
import { DailyLog, Mood, Efficiency } from '../../types';
import {
  COLORS,
  MOOD_EMOJIS,
  ENERGY_EMOJIS,
  EFFICIENCY_EMOJIS,
} from '../../constants';

interface CalendarDayProps {
  date: dayjs.Dayjs;
  log?: DailyLog;
  isToday?: boolean;
  onPress?: () => void;
}

export const CalendarDay: React.FC<CalendarDayProps> = ({
  date,
  log,
  isToday = false,
  onPress,
}) => {
  const dayName = date.format('ddd');
  const dayNum = date.format('D');

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

  return (
    <TouchableOpacity
      style={[
        styles.container,
        isToday && styles.todayContainer,
        log && { borderLeftWidth: 4, borderLeftColor: getMoodColor(log.mood) },
      ]}
      onPress={onPress}
      activeOpacity={0.7}
    >
      <Text style={[styles.dayName, isToday && styles.todayText]}>{dayName}</Text>
      <Text style={[styles.dayNum, isToday && styles.todayText]}>{dayNum}</Text>

      {log ? (
        <View style={styles.logContent}>
          <Text style={styles.moodEmoji}>{MOOD_EMOJIS[log.mood]}</Text>
          <Text style={styles.energyEmoji}>{ENERGY_EMOJIS[log.energy]}</Text>
          <View
            style={[
              styles.efficiencyDot,
              { backgroundColor: getEfficiencyColor(log.efficiency) },
            ]}
          />
        </View>
      ) : (
        <View style={styles.emptyContent}>
          <Text style={styles.emptyDot}>·</Text>
        </View>
      )}
    </TouchableOpacity>
  );
};

interface CalendarWeekProps {
  weekDays: dayjs.Dayjs[];
  logs: Map<string, DailyLog>;
  currentDate: dayjs.Dayjs;
  onDayPress?: (date: dayjs.Dayjs) => void;
}

export const CalendarWeek: React.FC<CalendarWeekProps> = ({
  weekDays,
  logs,
  currentDate,
  onDayPress,
}) => {
  const today = dayjs().format('YYYY-MM-DD');

  return (
    <View style={styles.weekContainer}>
      {weekDays.map(date => {
        const dateStr = date.format('YYYY-MM-DD');
        const log = logs.get(dateStr);
        const isToday = dateStr === today;

        return (
          <CalendarDay
            key={dateStr}
            date={date}
            log={log}
            isToday={isToday}
            onPress={() => onDayPress?.(date)}
          />
        );
      })}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    paddingVertical: 12,
    paddingHorizontal: 4,
    backgroundColor: COLORS.card,
    borderRadius: 12,
    marginHorizontal: 4,
    minHeight: 90,
  },
  todayContainer: {
    backgroundColor: COLORS.background,
    borderWidth: 1,
    borderColor: COLORS.border,
  },
  dayName: {
    fontSize: 12,
    color: COLORS.textSecondary,
    marginBottom: 4,
  },
  dayNum: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.text,
    marginBottom: 8,
  },
  todayText: {
    color: COLORS.text,
    fontWeight: '700',
  },
  logContent: {
    alignItems: 'center',
    gap: 2,
  },
  moodEmoji: {
    fontSize: 18,
  },
  energyEmoji: {
    fontSize: 10,
  },
  efficiencyDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    marginTop: 4,
  },
  emptyContent: {
    marginTop: 8,
  },
  emptyDot: {
    fontSize: 20,
    color: COLORS.border,
  },
  weekContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 12,
  },
});
