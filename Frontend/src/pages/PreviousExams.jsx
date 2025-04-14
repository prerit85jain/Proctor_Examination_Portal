import { useState } from 'react';

const PreviousExams = () => {
  const [exams] = useState([
    { id: 1, subject: 'Mathematics', date: '2024-03-01', score: '85%', status: 'Completed' },
    { id: 2, subject: 'Physics', date: '2024-02-28', score: '92%', status: 'Completed' },
    { id: 3, subject: 'Chemistry', date: '2024-02-25', score: '78%', status: 'Completed' },
  ]);

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Previous Exams</h1>
      
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="px-4 py-5 sm:p-6">
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Subject
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Date
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Score
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {exams.map((exam) => (
                  <tr key={exam.id}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {exam.subject}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {exam.date}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {exam.score}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-blue-100 text-blue-800">
                        {exam.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PreviousExams;