import React from 'react';
import { Calendar } from 'lucide-react';

/**
 * Sidebar component - displays years list for selection
 * Click on a year to view contests for that year
 */
interface SidebarProps {
  years: number[];
  selectedYear: number | null;
  onSelectYear: (year: number) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ years, selectedYear, onSelectYear }) => {
  return (
    <aside
      className="w-64 bg-white border-r border-gray-200 p-6 overflow-y-auto h-[calc(100vh-64px)]"
    >
      <h2 className="flex items-center gap-2 text-sm font-semibold text-gray-700 uppercase tracking-wide mb-6">
        <Calendar className="w-5 h-5" />
        Years
      </h2>

      <div className="space-y-2">
        {years.length === 0 ? (
          <p className="text-sm text-gray-500 text-center py-8">No years available</p>
        ) : (
          years.map((year) => (
            <button
              key={year}
              onClick={() => onSelectYear(year)}
              className={`w-full px-4 py-3 text-left rounded-lg font-semibold transition-all duration-200 flex items-center gap-3 ${
                selectedYear === year
                  ? 'bg-blue-600 text-white shadow-md'
                  : 'bg-gray-50 text-gray-900 hover:bg-gray-100'
              }`}
            >
              <Calendar className="w-5 h-5" />
              {year}
            </button>
          ))
        )}
      </div>
    </aside>
  );
};
