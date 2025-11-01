import { useAuthStore } from '@/store/authStore';
import { useEffect } from 'react';

export const useAuth = () => {
  const {
    user,
    token,
    isLoading,
    error,
    isAuthenticated,
    login,
    logout,
    clearError,
    initialize,
  } = useAuthStore();

  useEffect(() => {
    initialize();
  }, [initialize]);

  return {
    user,
    token,
    isLoading,
    error,
    isAuthenticated,
    login,
    logout,
    clearError,
  };
};
