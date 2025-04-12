import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import PreviousExams from './pages/PreviousExams';

function App() {
  const handleSearch = (query) => {
    console.log('Searching for:', query);
    // Implement search logic here
  };

  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route
          path="/dashboard"
          element={
            <Layout onSearch={handleSearch}>
              <Dashboard />
            </Layout>
          }
        />
        <Route
          path="/previous-exams"
          element={
            <Layout onSearch={handleSearch}>
              <PreviousExams />
            </Layout>
          }
        />
        <Route path="/" element={<Navigate to="/login" replace />} />
      </Routes>
    </Router>
  );
}

export default App;