import React, { useState, useEffect, useMemo } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  StatusBar,
} from 'react-native';
import { useNavigation } from '@react-navigation/native';
import dayjs from 'dayjs';
import { HomeScreenProps } from '../../types/navigation';
import { CheckInModal, CalendarWeek, WeekSummaryCard } from '../components';
import { COLORS } from '../constants';
import { getAllLogs, saveLog, hasLog } from '../utils/storage';
import { generateWeekSummary, getInsights } from '../utils/insights';
import { DailyLog, Mood, Efficiency } from '../types';

export const HomeScreen: React.FC<HomeScreenProps> = () => {
  const navigation = useNavigation();
  const [currentDate, setCurrentDate] = useState(dayjs());
  const [modalVisible, setModalVisible] = useState(false);
  const [logs, setLogs] = useState<Map<string, DailyLog>>(new Map());
  const [insights, setInsights] = useState<string[]>([]);

  // 加载数据
  useEffect(() => {
    const loadData = () => {
      const allLogs = getAllLogs();
      const logsMap = new Map<string, DailyLog>();
      allLogs.forEach(log => logsMap.set(log.date, log));
      setLogs(logsMap);

      const weekInsights = getInsights();
      setInsights(weekInsights.map(i => i.text));
    };

    loadData();
  }, []);

  // 当前周的日期
  const weekDays = useMemo(() => {
    const start = currentDate.startOf('isoWeek');
    return Array.from({ length: 7 }, (_, i) => start.add(i, 'day'));
  }, [currentDate]);

  // 周报摘要
  const weekSummary = useMemo(() => {
    return generateWeekSummary(currentDate.year(), currentDate.isoWeek());
  }, [currentDate, logs]);

  // 是否已打卡
  const todayLogged = hasLog(dayjs().format('YYYY-MM-DD'));

  const handleCheckIn = (mood: Mood, energy: 1 | 2 | 3 | 4, efficiency: Efficiency) => {
    const newLog: DailyLog = {
      date: dayjs().format('YYYY-MM-DD'),
      mood,
      energy,
      efficiency,
      createdAt: Date.now(),
    };

    saveLog(newLog);

    // 更新本地状态
    const newLogs = new Map(logs);
    newLogs.set(newLog.date, newLog);
    setLogs(newLogs);

    // 刷新洞察
    const newInsights = getInsights();
    setInsights(newInsights.map(i => i.text));
  };

  const navigateToWeekReport = () => {
    navigation.navigate('WeeklyReport', {
      year: currentDate.year(),
      weekNumber: currentDate.isoWeek(),
    });
  };

  const navigateToMonthView = () => {
    navigation.navigate('MonthlyCalendar', {
      year: currentDate.year(),
      month: currentDate.month() + 1,
    });
  };

  return (
    <View style={styles.container}>
      <StatusBar barStyle="dark-content" />

      {/* Header */}
      <View style={styles.header}>
        <View style={styles.logoRow}>
          <Text style={styles.logo}>🌸</Text>
          <Text style={styles.title}>她周期</Text>
        </View>
        <TouchableOpacity style={styles.settingsButton}>
          <Text style={styles.settingsIcon}>⚙️</Text>
        </TouchableOpacity>
      </View>

      <ScrollView style={styles.scrollView} showsVerticalScrollIndicator={false}>
        {/* Month Navigation */}
        <View style={styles.monthNav}>
          <TouchableOpacity
            onPress={() => setCurrentDate(currentDate.subtract(1, 'month'))}
          >
            <Text style={styles.navArrow}>←</Text>
          </TouchableOpacity>
          <Text style={styles.monthText}>
            {currentDate.format('YYYY 年 M 月')}
          </Text>
          <TouchableOpacity
            onPress={() => setCurrentDate(currentDate.add(1, 'month'))}
          >
            <Text style={styles.navArrow}>→</Text>
          </TouchableOpacity>
        </View>

        {/* Week Navigation */}
        <View style={styles.weekNav}>
          <TouchableOpacity
            onPress={() => setCurrentDate(currentDate.subtract(1, 'week'))}
          >
            <Text style={styles.navArrow}>←</Text>
          </TouchableOpacity>
          <Text style={styles.weekText}>
            第 {currentDate.isoWeek()} 周
          </Text>
          <TouchableOpacity
            onPress={() => setCurrentDate(currentDate.add(1, 'week'))}
          >
            <Text style={styles.navArrow}>→</Text>
          </TouchableOpacity>
        </View>

        {/* Calendar */}
        <View style={styles.calendarContainer}>
          <CalendarWeek
            weekDays={weekDays}
            logs={logs}
            currentDate={currentDate}
          />
        </View>

        {/* Week Summary Card */}
        <WeekSummaryCard summary={weekSummary} onPress={navigateToWeekReport} />

        {/* Insights */}
        {insights.length > 0 && (
          <View style={styles.insightsContainer}>
            <Text style={styles.sectionTitle}>💡 本周洞察</Text>
            {insights.map((insight, index) => (
              <View key={index} style={styles.insightItem}>
                <Text style={styles.insightText}>{insight}</Text>
              </View>
            ))}
          </View>
        )}

        {/* Check-in Button */}
        <View style={styles.checkInContainer}>
          <TouchableOpacity
            style={[
              styles.checkInButton,
              todayLogged && styles.checkInButtonLogged,
            ]}
            onPress={() => setModalVisible(true)}
            activeOpacity={0.8}
          >
            <Text style={styles.checkInIcon}>{todayLogged ? '✓' : '+'}</Text>
            <Text style={styles.checkInText}>
              {todayLogged ? '今日已打卡' : '今天打卡'}
            </Text>
          </TouchableOpacity>
        </View>

        {/* Month View Button */}
        <TouchableOpacity
          style={styles.monthViewButton}
          onPress={navigateToMonthView}
        >
          <Text style={styles.monthViewText}>📅 查看月度日历</Text>
        </TouchableOpacity>

        {/* Bottom Spacer */}
        <View style={styles.bottomSpacer} />
      </ScrollView>

      {/* Check-in Modal */}
      <CheckInModal
        visible={modalVisible}
        onClose={() => setModalVisible(false)}
        onSubmit={handleCheckIn}
      />
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
  logoRow: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  logo: {
    fontSize: 28,
    marginRight: 8,
  },
  title: {
    fontSize: 24,
    fontWeight: '700',
    color: COLORS.text,
  },
  settingsButton: {
    padding: 8,
  },
  settingsIcon: {
    fontSize: 20,
  },
  scrollView: {
    flex: 1,
  },
  monthNav: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: 20,
    marginBottom: 8,
  },
  navArrow: {
    fontSize: 20,
    paddingHorizontal: 16,
    color: COLORS.textSecondary,
  },
  monthText: {
    fontSize: 18,
    fontWeight: '600',
    color: COLORS.text,
  },
  weekNav: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: 20,
    marginBottom: 16,
  },
  weekText: {
    fontSize: 14,
    color: COLORS.textSecondary,
    paddingHorizontal: 16,
  },
  calendarContainer: {
    paddingHorizontal: 16,
    marginBottom: 20,
  },
  insightsContainer: {
    paddingHorizontal: 20,
    marginBottom: 20,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.text,
    marginBottom: 12,
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
  checkInContainer: {
    paddingHorizontal: 20,
    marginBottom: 16,
  },
  checkInButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: COLORS.happy,
    borderRadius: 16,
    paddingVertical: 16,
    shadowColor: COLORS.shadow,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 1,
    shadowRadius: 12,
    elevation: 4,
  },
  checkInButtonLogged: {
    backgroundColor: COLORS.high,
  },
  checkInIcon: {
    fontSize: 20,
    fontWeight: '700',
    color: '#fff',
    marginRight: 8,
  },
  checkInText: {
    fontSize: 18,
    fontWeight: '600',
    color: '#fff',
  },
  monthViewButton: {
    alignItems: 'center',
    paddingVertical: 12,
  },
  monthViewText: {
    fontSize: 14,
    color: COLORS.textSecondary,
  },
  bottomSpacer: {
    height: 40,
  },
});
