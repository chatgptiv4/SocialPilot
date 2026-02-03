import { Route, Routes } from 'react-router-dom';
import DashboardLayout from './layouts/DashboardLayout';
import ChatPage from './pages/ChatPage';
import BrandPage from './pages/BrandPage';
import PosterPage from './pages/PosterPage';
import CampaignPage from './pages/CampaignPage';
import SchedulerPage from './pages/SchedulerPage';
import AnalyticsPage from './pages/AnalyticsPage';
import ConnectedAccountsPage from './pages/ConnectedAccountsPage';

export default function App() {
  return (
    <DashboardLayout>
      <Routes>
        <Route path="/" element={<ChatPage />} />
        <Route path="/brand-dna" element={<BrandPage />} />
        <Route path="/poster-generator" element={<PosterPage />} />
        <Route path="/campaigns" element={<CampaignPage />} />
        <Route path="/scheduler" element={<SchedulerPage />} />
        <Route path="/analytics" element={<AnalyticsPage />} />
        <Route path="/connected-accounts" element={<ConnectedAccountsPage />} />
      </Routes>
    </DashboardLayout>
  );
}
