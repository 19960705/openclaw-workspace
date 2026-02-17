import dayjs from 'dayjs';
import { STORAGE_KEYS } from '../constants';
import { DailyLog, Mood, Efficiency } from '../types';

// 初始化 MMKV（原生模块）
let Storage: any = null;

try {
  const MMKV = require('mmkv');
  Storage = new MMKV.default();
} catch (e) {
  // Web 环境降级
  Storage = {
    getString: (key: string) => {
      if (typeof window !== 'undefined' && window.localStorage) {
        return window.localStorage.getItem(key);
      }
      return null;
    },
    set: (key: string, value: string) => {
      if (typeof window !== 'undefined' && window.localStorage) {
        window.localStorage.setItem(key, value);
      }
    },
  };
}

// 读取所有打卡记录
export const getAllLogs = (): DailyLog[] => {
  try {
    const data = Storage.getString(STORAGE_KEYS.DAILY_LOGS);
    if (!data) return [];
    return JSON.parse(data);
  } catch {
    return [];
  }
};

// 保存打卡记录
export const saveLog = (log: DailyLog): void => {
  try {
    const logs = getAllLogs();
    const existingIndex = logs.findIndex(l => l.date === log.date);

    if (existingIndex >= 0) {
      logs[existingIndex] = log;
    } else {
      logs.push(log);
    }

    Storage.set(STORAGE_KEYS.DAILY_LOGS, JSON.stringify(logs));
  } catch (e) {
    console.error('Failed to save log:', e);
  }
};

// 获取某天的打卡记录
export const getLogByDate = (date: string): DailyLog | null => {
  const logs = getAllLogs();
  return logs.find(l => l.date === date) || null;
};

// 获取某周的所有记录
export const getLogsByWeek = (year: number, weekNumber: number): DailyLog[] => {
  const logs = getAllLogs();
  return logs.filter(l => {
    const d = dayjs(l.date);
    return d.year() === year && d.week() === weekNumber;
  });
};

// 获取某月的所有记录
export const getLogsByMonth = (year: number, month: number): DailyLog[] => {
  const logs = getAllLogs();
  return logs.filter(l => {
    const d = dayjs(l.date);
    return d.year() === year && d.month() === month;
  });
};

// 删除某天的记录
export const deleteLog = (date: string): void => {
  try {
    const logs = getAllLogs();
    const filtered = logs.filter(l => l.date !== date);
    Storage.set(STORAGE_KEYS.DAILY_LOGS, JSON.stringify(filtered));
  } catch (e) {
    console.error('Failed to delete log:', e);
  }
};

// 检查某天是否已打卡
export const hasLog = (date: string): boolean => {
  return getLogByDate(date) !== null;
};
