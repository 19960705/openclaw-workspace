import { NativeStackScreenProps } from '@react-navigation/native-stack';
import { BottomTabScreenProps } from '@react-navigation/bottom-tabs';

// Root Stack Navigator
export type RootStackParamList = {
  Home: undefined;
  WeeklyReport: { year: number; weekNumber: number };
  MonthlyCalendar: { year: number; month: number };
  Settings: undefined;
};

// 屏幕Props类型
export type HomeScreenProps = NativeStackScreenProps<RootStackParamList, 'Home'>;
export type WeeklyReportScreenProps = NativeStackScreenProps<RootStackParamList, 'WeeklyReport'>;
export type MonthlyCalendarScreenProps = NativeStackScreenProps<RootStackParamList, 'MonthlyCalendar'>;
export type SettingsScreenProps = NativeStackScreenProps<RootStackParamList, 'Settings'>;
