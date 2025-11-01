export const API_URL = import.meta.env.VITE_API_URL || '/api';
export const APP_NAME = import.meta.env.VITE_APP_NAME || 'Platform Zarządzania Projektami';

export const ROUTES = {
  HOME: '/',
  LOGIN: '/login',
  DASHBOARD: '/dashboard',
  TASKS: '/tasks',
  TASKS_CREATE: '/tasks/create',
} as const;

export const STORAGE_KEYS = {
  AUTH_TOKEN: 'auth_token',
  USER_DATA: 'user_data',
  THEME: 'theme',
} as const;

export const TASK_STATUS = {
  TODO: 'todo',
  IN_PROGRESS: 'in_progress',
  REVIEW: 'review',
  DONE: 'done',
} as const;

export const TASK_PRIORITY = {
  LOW: 'low',
  MEDIUM: 'medium',
  HIGH: 'high',
  URGENT: 'urgent',
} as const;

export const QUERY_KEYS = {
  TASKS: 'tasks',
  TASK: 'task',
  USER: 'user',
  USERS: 'users',
} as const;
