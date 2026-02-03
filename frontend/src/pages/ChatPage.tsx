import { useState } from 'react';

export default function ChatPage() {
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState<string[]>(["Welcome to the AI Command Center."]);

  const handleSend = () => {
    if (!message.trim()) return;
    setMessages(prev => [...prev, `You: ${message}`, `AI: Working on "${message}"`]);
    setMessage('');
  };

  return (
    <section>
      <h2 className="text-2xl font-semibold mb-4">AI Chat Command Center</h2>
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
