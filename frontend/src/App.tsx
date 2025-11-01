import React, { useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MainLayout } from '@/components/layout/MainLayout';
import { Login } from '@/pages/Login/Login';
import { Dashboard } from '@/pages/Dashboard/Dashboard';
import { TaskList } from '@/pages/Tasks/TaskList';
import { TaskCreate } from '@/pages/Tasks/TaskCreate';
import { useAuth } from '@/hooks/useAuth';
import { ROUTES } from '@/utils/constants';
import { offlineService } from '@/services/offline';
import { setUnauthorizedHandler } from '@/services/api';

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5 * 60 * 1000, // 5 minutes
    },
  },
});

// Protected Route Component
const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated } = useAuth();
  
  if (!isAuthenticated) {
    return <Navigate to={ROUTES.LOGIN} replace />;
  }
  
  return <>{children}</>;
};

// Component to set up unauthorized handler
const AppInitializer: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const navigate = useNavigate();

  useEffect(() => {
    // Set up unauthorized handler
    setUnauthorizedHandler(() => {
      navigate(ROUTES.LOGIN, { replace: true });
    });
  }, [navigate]);

  return <>{children}</>;
};

function App() {
  useEffect(() => {
    // Initialize offline service
    offlineService.getOnlineStatus();
  }, []);

  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <AppInitializer>
          <Routes>
            <Route path={ROUTES.LOGIN} element={<Login />} />
          
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <MainLayout />
              </ProtectedRoute>
            }
          >
            <Route index element={<Navigate to={ROUTES.DASHBOARD} replace />} />
            <Route path={ROUTES.DASHBOARD} element={<Dashboard />} />
            <Route path={ROUTES.TASKS} element={<TaskList />} />
            <Route path={ROUTES.TASKS_CREATE} element={<TaskCreate />} />
          </Route>

          {/* Fallback route */}
          <Route path="*" element={<Navigate to={ROUTES.DASHBOARD} replace />} />
          </Routes>
        </AppInitializer>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
