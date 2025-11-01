import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card } from '@/components/common/Card';
import { LoginForm } from '@/components/forms/LoginForm';
import { useAuth } from '@/hooks/useAuth';
import { ROUTES } from '@/utils/constants';

export const Login: React.FC = () => {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();

  useEffect(() => {
    if (isAuthenticated) {
      navigate(ROUTES.DASHBOARD);
    }
  }, [isAuthenticated, navigate]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-50 to-primary-100 px-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Platform Zarządzania Projektami
          </h1>
          <p className="text-gray-600">
            Sign in to access your projects
          </p>
        </div>
        
        <Card>
          <LoginForm />
        </Card>

        <div className="mt-4 text-center text-sm text-gray-600">
          <p>System zarządzania projektami telekomunikacyjnymi</p>
        </div>
      </div>
    </div>
  );
};
