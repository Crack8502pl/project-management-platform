import React from 'react';

export const Footer: React.FC = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-white border-t border-gray-200 mt-auto">
      <div className="px-4 py-4">
        <div className="flex flex-col sm:flex-row items-center justify-between gap-2 text-sm text-gray-600">
          <p>© {currentYear} Platform Zarządzania Projektami. All rights reserved.</p>
          <p className="text-gray-500">Version 1.0.0</p>
        </div>
      </div>
    </footer>
  );
};
