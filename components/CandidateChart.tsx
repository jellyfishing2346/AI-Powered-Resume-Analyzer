import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { CandidateAnalysis } from '../types';

interface Props {
  data: CandidateAnalysis[];
}

export const CandidateChart: React.FC<Props> = ({ data }) => {
  const chartData = [...data].sort((a, b) => b.score - a.score).slice(0, 10);

  return (
    <div className="h-64 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} />
          <XAxis dataKey="candidateName" fontSize={10} interval={0} />
          <YAxis domain={[0, 100]} />
          <Tooltip 
            contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
          />
          <Bar dataKey="score" radius={[4, 4, 0, 0]}>
            {chartData.map((entry, index) => (
              <Cell 
                key={`cell-${index}`} 
                fill={entry.score > 80 ? '#4f46e5' : entry.score > 50 ? '#6366f1' : '#a5b4fc'} 
              />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};
