import { LayoutDashboard, ClipboardList, ChevronLeft } from 'lucide-react';
import { NavLink } from 'react-router-dom';

const Sidebar = ({ isOpen, setIsOpen }) => {
  const menuItems = [
    { icon: LayoutDashboard, text: 'Dashboard', path: '/dashboard' },
    { icon: ClipboardList, text: 'Previous Exams', path: '/previous-exams' },
  ];

  return (
    <div className={`h-screen bg-gray-900 text-white fixed left-0 top-0 z-30 transition-all duration-300 ${isOpen ? 'w-64' : 'w-0'}`}>
      <div className="p-4 h-full overflow-hidden">
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-2xl font-bold">Exam Board</h1>
          <button 
            onClick={() => setIsOpen(false)}
            className="lg:hidden text-gray-300 hover:text-white"
          >
            <ChevronLeft size={20} />
          </button>
        </div>
        <nav>
          {menuItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center space-x-3 p-3 rounded-lg transition-colors ${
                  isActive
                    ? 'bg-blue-600 text-white'
                    : 'text-gray-300 hover:bg-gray-800'
                }`
              }
            >
              <item.icon size={20} />
              <span>{item.text}</span>
            </NavLink>
          ))}
        </nav>
      </div>
    </div>
  );
};

export default Sidebar;