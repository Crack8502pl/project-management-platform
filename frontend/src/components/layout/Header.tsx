import React from 'react';
import { useAuth } from '@/hooks/useAuth';
import { APP_NAME } from '@/utils/constants';

interface HeaderProps {
  onMenuClick: () => void;
  showMenuButton: boolean;
}

export const Header: React.FC<HeaderProps> = ({ onMenuClick, showMenuButton }) => {
  const { user, logout } = useAuth();

  return (
    <header className="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-40">
      <div className="flex items-center justify-between h-16 px-4">
        <div className="flex items-center gap-4">
          {showMenuButton && (
            <button
              onClick={onMenuClick}
              className="p-2 rounded-md hover:bg-gray-100 lg:hidden"
              aria-label="Open menu"
            >
              <svg
                className="w-6 h-6"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 6h16M4 12h16M4 18h16"
                />
              </svg>
            </button>
          )}
          <h1 className="text-xl font-semibold text-gray-900 truncate">
            {APP_NAME}
          </h1>
        </div>

        <div className="flex items-center gap-4">
          {user && (
            <>
              <span className="hidden sm:block text-sm text-gray-700">
                {user.firstName} {user.lastName}
              </span>
              <button
                onClick={logout}
                className="px-3 py-1.5 text-sm text-gray-700 hover:text-gray-900 hover:bg-gray-100 rounded-md"
              >
                Logout
              </button>
            </>
          )}
        </div>
      </div>
    </header>
  );
};
