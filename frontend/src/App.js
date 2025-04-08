import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout.jsx';

// Page imports
import Home from './pages/Home';
import Overview from './pages/Overview';
import Balances from './pages/Balances';
import Transactions from './pages/Transactions';
import Bills from './pages/Bills';
import Expenses from './pages/Expenses';
import Goals from './pages/Goals';
import Settings from './pages/Settings';
import Login from './pages/Login';
import Register from './pages/Register';

function App() {
  return (
    <Router>
      <Routes>
        {/* Layout-wrapped dashboard pages */}
        <Route element={<Layout />}>
          <Route path="/overview" element={<Overview />} />
          <Route path="/balances" element={<Balances />} />
          <Route path="/transactions" element={<Transactions />} />
          <Route path="/bills" element={<Bills />} />
          <Route path="/expenses" element={<Expenses />} />
          <Route path="/goals" element={<Goals />} />
          <Route path="/settings" element={<Settings />} />
        </Route>

        {/* Public pages */}
        <Route path="/" element={<Navigate to="/overview" replace />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
      </Routes>
    </Router>
  );
}

export default App;