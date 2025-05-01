import { X, BookOpen, Users, Calendar, Clock } from 'lucide-react';

const SubjectDetails = ({ subject, onClose }) => {
  if (!subject) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl shadow-xl w-full max-w-2xl">
        <div className="p-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-gray-900">{subject.name}</h2>
            <button
              onClick={onClose}
              className="p-2 hover:bg-gray-100 rounded-full transition-colors"
            >
              <X size={20} className="text-gray-500" />
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            <div className="flex items-center space-x-3 p-4 bg-blue-50 rounded-lg">
              <Calendar className="text-blue-600" size={24} />
              <div>
                <p className="text-sm text-gray-600">Exam Date</p>
                <p className="font-semibold text-gray-900">{subject.examDate}</p>
              </div>
            </div>
            <div className="flex items-center space-x-3 p-4 bg-green-50 rounded-lg">
              <Users className="text-green-600" size={24} />
              <div>
                <p className="text-sm text-gray-600">Enrolled Students</p>
                <p className="font-semibold text-gray-900">{subject.students}</p>
              </div>
            </div>
            <div className="flex items-center space-x-3 p-4 bg-purple-50 rounded-lg">
              <BookOpen className="text-purple-600" size={24} />
              <div>
                <p className="text-sm text-gray-600">Topics Covered</p>
                <p className="font-semibold text-gray-900">{subject.topics}</p>
              </div>
            </div>
            <div className="flex items-center space-x-3 p-4 bg-orange-50 rounded-lg">
              <Clock className="text-orange-600" size={24} />
              <div>
                <p className="text-sm text-gray-600">Duration</p>
                <p className="font-semibold text-gray-900">3 hours</p>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-gray-900">Syllabus Overview</h3>
            <div className="bg-gray-50 p-4 rounded-lg">
              <ul className="list-disc list-inside space-y-2 text-gray-600">
                <li>Introduction to {subject.name}</li>
                <li>Core Concepts and Fundamentals</li>
                <li>Advanced Topics and Applications</li>
                <li>Problem Solving Techniques</li>
                <li>Practical Implementations</li>
              </ul>
            </div>
          </div>

          <div className="mt-8 flex justify-end space-x-4">
            <button
              onClick={onClose}
              className="px-4 py-2 text-gray-600 hover:text-gray-800"
            >
              Close
            </button>
            <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
              Edit Details
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SubjectDetails;