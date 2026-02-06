export default function AnalyticsPage() {
  return (
    <section className="space-y-4">
      <h2 className="text-2xl font-semibold">Analytics</h2>
      <div className="grid gap-4 md:grid-cols-3">
        <div className="bg-slate-900 border border-slate-800 rounded p-4">
          <h3 className="font-semibold">Engagement</h3>
          <p className="text-sm text-slate-300">Track impressions, clicks, likes, and comments.</p>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded p-4">
          <h3 className="font-semibold">AI Suggestions</h3>
          <p className="text-sm text-slate-300">Get actionable optimization insights.</p>
        </div>
      </div>
    </section>
  );
}
