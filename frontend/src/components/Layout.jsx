import React, { useState } from 'react';
import { NavLink, Outlet, useNavigate, useLocation } from 'react-router-dom';
import {
  CalendarDays, Search, LogOut, LayoutDashboard,
  Wallet, CreditCard, LineChart, Trophy, Settings
} from 'lucide-react';

const sidebarLinks = [
  { name: 'Overview', icon: <LayoutDashboard size={16} />, path: '/overview' },
  { name: 'Balances', icon: <Wallet size={16} />, path: '/balances' },
  { name: 'Transactions', icon: <CreditCard size={16} />, path: '/transactions' },
  { name: 'Bills', icon: <CreditCard size={16} />, path: '/bills' },
  { name: 'Expenses', icon: <LineChart size={16} />, path: '/expenses' },
  { name: 'Goals', icon: <Trophy size={16} />, path: '/goals' },
  { name: 'Settings', icon: <Settings size={16} />, path: '/settings' },
  { name: 'Logout', icon: <LogOut size={16} />, path: '/logout' }
];

export default function Layout() {
  const navigate = useNavigate();
  const location = useLocation();
  const currentDate = new Date().toLocaleDateString(undefined, {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });

  const [search, setSearch] = useState('');

  const handleSearch = (e) => {
    const value = e.target.value;
    setSearch(value);

    const params = new URLSearchParams(location.search);
    if (value) {
      params.set('search', value);
    } else {
      params.delete('search');
    }

    navigate(`${location.pathname}?${params.toString()}`, { replace: true });
  };

  return (
    <div className="flex h-screen overflow-hidden">
      {/* Sidebar */}
      <aside className="w-64 bg-[#111827] text-white flex flex-col justify-between">
        <div>
          <h2 className="text-2xl font-bold p-6 border-b border-gray-700">WEALTHWISE</h2>
          <nav className="mt-4 space-y-2 px-4">
            {sidebarLinks.map((link) => (
              <NavLink
                to={link.path}
                key={link.name}
                className={({ isActive }) =>
                  `flex items-center gap-2 px-3 py-2 rounded transition ${
                    isActive ? 'bg-blue-600 text-white' : 'text-gray-300 hover:bg-gray-800'
                  }`
                }
              >
                {link.icon}
                <span>{link.name}</span>
              </NavLink>
            ))}
          </nav>
        </div>
        <div className="p-4 border-t border-gray-700 text-sm text-gray-400">
          <div className="bg-gray-800 rounded-full w-full py-2 px-4 flex items-center justify-between">
            <span className="text-white font-semibold">KA</span>
            <span className="text-gray-400">kaartikeya</span>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 bg-gray-50 p-6 overflow-y-auto">
        <div className="flex justify-between items-center mb-6">
          <div className="flex items-center gap-2 text-gray-600 text-sm">
            <CalendarDays size={16} />
            <span>{currentDate}</span>
          </div>
          <div className="flex items-center gap-2">
            <Search size={16} className="text-gray-400" />
            <input
              type="text"
              placeholder="Search here"
              value={search}
              onChange={handleSearch}
              className="border border-gray-300 rounded px-3 py-1 text-sm focus:outline-none"
            />
          </div>
        </div>

        <Outlet />
      </main>
    </div>
  );
}