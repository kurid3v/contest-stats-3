import React, { useState, useEffect } from 'react';
import { Header } from '../components/Header';
import { Sidebar } from '../components/Sidebar';
import { ContestCard } from '../components/ContestCard';
import { api } from '../lib/api';

/**
 * HomePage - Main page displaying contests organized by class and year
 * Features class selection, sidebar with years, and contest cards for selected year
 */
interface Contest {
  id: number;
  class_level: number;
  year: number;
  pre_number: number;
  contest_url: string;
  solution_url: string;
}

export const HomePage: React.FC = () => {
  const [selectedClass, setSelectedClass] = useState<number>(9);
  const [selectedYear, setSelectedYear] = useState<number | null>(null);
  const [contests, setContests] = useState<Contest[]>([]);
  const [loading, setLoading] = useState(false);

  // Fetch contests on component mount
  useEffect(() => {
    fetchContests();
  }, []);

  // Set default year when contests are loaded or class changes
  useEffect(() => {
    if (contests.length > 0 && selectedClass) {
      const filteredContests = contests.filter(c => c.class_level === selectedClass);
      const years = [...new Set(filteredContests.map(c => c.year))].sort((a, b) => b - a);
      if (years.length > 0 && !selectedYear) {
        setSelectedYear(years[0]);
      }
    }
  }, [contests, selectedClass]);

  const fetchContests = async () => {
    try {
      setLoading(true);
      const response = await api.get('/contests');
      setContests(response.data);
    } catch (error) {
      console.error('Failed to fetch contests:', error);
    } finally {
      setLoading(false);
    }
  };

  // Filter contests by selected class and year
  const filteredContests = contests.filter(
    c => c.class_level === selectedClass && (selectedYear === null || c.year === selectedYear)
  );

  // Group contests by year for sidebar
  const contestsByYear = contests.filter(c => c.class_level === selectedClass).reduce((acc, contest) => {
    if (!acc[contest.year]) {
      acc[contest.year] = [];
    }
    acc[contest.year].push(contest);
    return acc;
  }, {} as Record<number, Contest[]>);

  return (
    <div className="min-h-screen bg-background">
      <Header selectedClass={selectedClass} onSelectClass={setSelectedClass} />

      <div className="flex">
        {selectedClass && (
          <Sidebar 
            years={Object.keys(contestsByYear).map(Number).sort((a, b) => b - a)}
            selectedYear={selectedYear}
            onSelectYear={setSelectedYear}
          />
        )}

        {/* Main content */}
        <main className="flex-1 p-6">
          <div>
            {loading ? (
              <div className="flex items-center justify-center h-64">
                <p className="text-gray-500">Loading contests...</p>
              </div>
            ) : selectedYear === null ? (
              <div className="flex items-center justify-center h-64">
                <p className="text-gray-500">Select a year from the sidebar to view contests</p>
              </div>
            ) : filteredContests.length === 0 ? (
              <div className="flex items-center justify-center h-64">
                <p className="text-gray-500">No contests available for this year.</p>
              </div>
            ) : (
              <div>
                <h2 className="text-2xl font-bold text-gray-900 mb-2">
                  Class {selectedClass} - Year {selectedYear}
                </h2>
                <p className="text-gray-600 text-sm mb-8">
                  {filteredContests.length} contest{filteredContests.length !== 1 ? 's' : ''} found
                </p>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {filteredContests
                    .sort((a, b) => a.pre_number - b.pre_number)
                    .map((contest) => (
                      <ContestCard
                        key={contest.id}
                        contestName={`PREHSG ${contest.year} Class ${contest.class_level}`}
                        preNumber={contest.pre_number}
                        contestUrl={contest.contest_url}
                        solutionUrl={contest.solution_url}
                      />
                    ))}
                </div>
              </div>
            )}
          </div>
        </main>
      </div>
    </div>
  );
};
