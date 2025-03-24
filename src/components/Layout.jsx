import Sidebar from './Sidebar';
import Header from './Header';
import { useState } from 'react';

const Layout = ({ children, onSearch }) => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);

  return (
    <div className="min-h-screen bg-gray-50">
      <Sidebar isOpen={isSidebarOpen} setIsOpen={setIsSidebarOpen} />
      <div className={`transition-all duration-300 ${isSidebarOpen ? 'ml-64' : 'ml-0'}`}>
        <Header onSearch={onSearch} toggleSidebar={() => setIsSidebarOpen(!isSidebarOpen)} />
        <main className="pt-24 px-4 sm:px-6 lg:px-8 pb-8">{children}</main>
      </div>
    </div>
  );
};

export default Layout;