import { NavLink } from 'react-router-dom';

const navItems = [
  { path: '/', label: 'Chat' },
  { path: '/brand-dna', label: 'Brand DNA Settings' },
  { path: '/poster-generator', label: 'Poster Generator' },
  { path: '/campaigns', label: 'Campaigns' },
  { path: '/scheduler', label: 'Scheduler Calendar' },
  { path: '/analytics', label: 'Analytics' },
  { path: '/connected-accounts', label: 'Connected Accounts' }
];

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen flex">
      <aside className="w-64 bg-slate-900 p-6 border-r border-slate-800">
        <h1 className="text-xl font-semibold mb-8">SocialPilot AI</h1>
        <nav className="flex flex-col gap-3">
          {navItems.map(item => (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `rounded px-3 py-2 text-sm ${isActive ? 'bg-indigo-600' : 'hover:bg-slate-800'}`
              }
              end={item.path === '/'}
            >
              {item.label}
            </NavLink>
          ))}
        </nav>
      </aside>
      <main className="flex-1 p-8 bg-slate-950">
        {children}
      </main>
    </div>
  );
}
