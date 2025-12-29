import React from 'react';
import { View } from '../types';

interface LayoutProps {
  children: React.ReactNode;
  currentView: View;
  onViewChange: (view: View) => void;
}

export const Layout: React.FC<LayoutProps> = ({ children, currentView, onViewChange }) => {
  const navItems: { id: View; label: string }[] = [
    { id: 'analyzer', label: 'Resume Analyzer' },
    { id: 'pipeline', label: 'Pipeline' },
    { id: 'settings', label: 'Settings' },
  ];

  return (
    <div className="min-h-screen flex flex-col">
      <header className="bg-white border-b sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <div 
              className="flex items-center space-x-2 cursor-pointer" 
              onClick={() => onViewChange('analyzer')}
            >
              <div className="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center shadow-sm">
                <span className="text-white font-bold">A</span>
              </div>
              <h1 className="text-xl font-bold text-gray-900 tracking-tight">
                Aura <span className="text-indigo-600">AI</span>
              </h1>
            </div>
            
            <nav className="hidden md:flex space-x-2">
              {navItems.map((item) => (
                <button
                  key={item.id}
                  onClick={() => onViewChange(item.id)}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                    currentView === item.id
                      ? 'bg-indigo-50 text-indigo-700 shadow-sm ring-1 ring-indigo-100'
                      : 'text-gray-500 hover:text-gray-900 hover:bg-gray-50'
                  }`}
                >
                  {item.label}
                </button>
              ))}
            </nav>

            <div className="flex items-center space-x-4">
              <div className="hidden sm:flex items-center space-x-2 text-[10px] text-gray-400 font-mono bg-gray-50 px-2 py-1 rounded-full border">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
                <span>API: ACTIVE</span>
              </div>
            </div>
          </div>
        </div>
      </header>
      <main className="flex-1 max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-8">
        {children}
      </main>
      <footer className="bg-white border-t py-6 mt-auto">
        <div className="max-w-7xl mx-auto px-4 text-center text-sm text-gray-500">
          &copy; 2024 Aura Intelligence. Advanced NLP Resume Parser.
        </div>
      </footer>
    </div>
  );
};