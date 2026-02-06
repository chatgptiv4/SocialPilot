import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { fetchHealth } from '../api/health';

export default function ChatPage() {
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState<string[]>(["Welcome to the AI Command Center."]);
  const { data: health, isLoading } = useQuery({
    queryKey: ['health'],
    queryFn: fetchHealth,
    refetchInterval: 10000
  });

  const handleSend = () => {
    if (!message.trim()) return;
    setMessages(prev => [...prev, `You: ${message}`, `AI: Working on "${message}"`]);
    setMessage('');
  };

  return (
    <section className="space-y-6">
      <h2 className="text-2xl font-semibold mb-4">AI Chat Command Center</h2>
      <div className="bg-slate-900 border border-slate-800 rounded p-4">
        <h3 className="font-semibold mb-2">System Health</h3>
        {isLoading ? (
          <p className="text-sm text-slate-300">Checking services...</p>
        ) : (
          <div className="flex gap-6 text-sm">
            <div>
              <span className="text-slate-400">Postgres:</span>{' '}
              <span className={health?.database.startsWith('ok') ? 'text-emerald-400' : 'text-rose-400'}>
                {health?.database ?? 'unknown'}
              </span>
            </div>
            <div>
              <span className="text-slate-400">Redis:</span>{' '}
              <span className={health?.redis.startsWith('ok') ? 'text-emerald-400' : 'text-rose-400'}>
                {health?.redis ?? 'unknown'}
              </span>
            </div>
          </div>
        )}
      </div>
      <div className="bg-slate-900 border border-slate-800 rounded p-4 h-96 overflow-y-auto">
        {messages.map((item, idx) => (
          <div key={idx} className="mb-2 text-sm text-slate-200">
            {item}
          </div>
        ))}
      </div>
      <div className="mt-4 flex gap-2">
        <input
          value={message}
          onChange={event => setMessage(event.target.value)}
          className="flex-1 rounded bg-slate-900 border border-slate-700 p-2 text-sm"
          placeholder="Create a Black Friday campaign"
        />
        <button onClick={handleSend} className="bg-indigo-600 px-4 py-2 rounded text-sm">
          Send
        </button>
      </div>
    </section>
  );
}
