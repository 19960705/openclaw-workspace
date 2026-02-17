// 颜色定义
export const COLORS = {
  // 情绪颜色
  happy: '#FFB5A7',    // 开心 - 柔和粉橘
  okay: '#FCD5CE',     // 一般 - 浅粉
  tired: '#F8EDEB',    // 疲惫 - 暖白
  crashed: '#D8A48F',  // 崩溃 - 深橘

  // 效率颜色
  high: '#B5E48C',     // 高效 - 绿色
  medium: '#FFD6A5',   // 中效 - 橙色
  low: '#FFADAD',      // 低效 - 红色

  // 背景
  background: '#FFF8F5',
  card: '#FFFFFF',
  text: '#2D3436',
  textSecondary: '#636E72',

  // UI
  border: '#FFE5D9',
  shadow: 'rgba(0,0,0,0.05)',
};

// 表情映射
export const MOOD_EMOJIS = {
  happy: '😊',
  okay: '😐',
  tired: '😫',
  crashed: '🤯',
};

export const MOOD_LABELS = {
  happy: '开心',
  okay: '一般',
  tired: '疲惫',
  crashed: '崩溃',
};

// 精力映射
export const ENERGY_EMOJIS = {
  1: '🔋',
  2: '🔋🔋',
  3: '🔋🔋🔋',
  4: '🔋🔋🔋🔋',
};

export const ENERGY_LABELS = {
  1: '很低',
  2: '偏低',
  3: '正常',
  4: '充满',
};

// 效率映射
export const EFFICIENCY_EMOJIS = {
  high: '🚀',
  medium: '⚡',
  low: '🐢',
};

export const EFFICIENCY_LABELS = {
  high: '高效',
  medium: '正常',
  low: '偏低',
};

// 存储 Key
export const STORAGE_KEYS = {
  DAILY_LOGS: 'daily_logs',
  SETTINGS: 'settings',
};
