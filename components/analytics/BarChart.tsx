import React from 'react';

interface ChartData {
  topicTitle: string;
  averageScore: number;
}

interface BarChartProps {
  data: ChartData[];
}

const BarChart: React.FC<BarChartProps> = ({ data }) => {
  if (!data || data.length === 0) {
    return (
        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md text-center">
            <h3 className="text-lg font-semibold text-gray-800 dark:text-white mb-4">Average Score per Topic</h3>
            <p className="text-gray-500 dark:text-gray-400 py-8">No data available for chart.</p>
        </div>
    );
  }

  const maxValue = 100; // Scores are percentages

  return (
    <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md">
       <h3 className="text-lg font-semibold text-gray-800 dark:text-white mb-4">Average Score per Topic</h3>
       <div className="flex justify-around items-end h-64 space-x-2 border-l-2 border-b-2 border-gray-200 dark:border-gray-700 pl-4 pb-4">
        {data.map(({ topicTitle, averageScore }) => (
          <div key={topicTitle} className="flex flex-col items-center flex-1 h-full justify-end">
            <div 
              className="w-10/12 bg-indigo-500 hover:bg-indigo-600 transition-all duration-300 rounded-t-md relative group" 
              style={{ height: `${(averageScore / maxValue) * 100}%` }}
              title={`${topicTitle}: ${averageScore}%`}
            >
                <span className="absolute -top-6 left-1/2 -translate-x-1/2 text-xs font-bold text-gray-700 dark:text-gray-200 opacity-0 group-hover:opacity-100 transition-opacity">
                    {averageScore}%
                </span>
            </div>
            <span className="text-xs text-gray-500 dark:text-gray-400 mt-2 text-center w-full" style={{ wordBreak: 'break-word' }}>
                {topicTitle}
            </span>
          </div>
        ))}
       </div>
    </div>
  );
};

export default BarChart;
