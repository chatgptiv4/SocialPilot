export default function BrandPage() {
  return (
    <section className="space-y-4">
      <h2 className="text-2xl font-semibold">Brand DNA Settings</h2>
      <div className="grid gap-4 md:grid-cols-2">
        <div className="bg-slate-900 border border-slate-800 rounded p-4">
          <h3 className="font-semibold mb-2">Profile</h3>
          <p className="text-sm text-slate-300">Capture brand name, niche, target audience, and tone.</p>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded p-4">
          <h3 className="font-semibold mb-2">Assets</h3>
          <p className="text-sm text-slate-300">Upload logos, backgrounds, and configure watermark rules.</p>
        </div>
      </div>
    </section>
  );
}
