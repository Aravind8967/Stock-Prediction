import React, { useState, useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import './AIChat.css'


// LLM Console Component
export function LLMConsole() {
    const [messages, setMessages] = useState([
        { sender: 'bot', text: "Hello! I'm your GenAI assistant. How can I help you today?" }
    ]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const chatBoxRef = useRef(null);

    useEffect(() => {
        if (chatBoxRef.current) {
            chatBoxRef.current.scrollTop = chatBoxRef.current.scrollHeight;
        }
    }, [messages]);

    const handleSubmit = async () => {
        if (!input.trim()) return;
        const userMsg = { sender: 'user', text: input.trim() };
        setMessages(prev => [...prev, userMsg]);
        setInput('');
        setLoading(true);

        const response = await askLLM(userMsg.text);
        setLoading(false);

        setMessages(prev => [...prev, { sender: 'bot', text: response || 'Failed to get an answer.' }]);
    };

    const handleKeyDown = e => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSubmit();
        }
    };

    return (
        <div className="container my-4">
            <div className="card shadow-sm">
                <div className="card-header bg-primary text-white d-flex justify-content-between align-items-center">
                    <h5 className="mb-0">AI Assistant</h5>
                </div>
                <div ref={chatBoxRef} className="card-body bg-light" style={{ height: '60vh', overflowY: 'auto' }}>
                    {messages.map((msg, idx) => (
                        <div
                            key={idx}
                            className={`chat-bubble ${msg.sender}`}
                        >
                            {msg.sender === 'bot'
                                ? <ReactMarkdown remarkPlugins={[remarkGfm]}>{msg.text}</ReactMarkdown>
                                : msg.text
                            }
                        </div>
                    ))}
                    {loading && <div className="text-muted fst-italic">Thinking...</div>}
                </div>
                <div className="card-footer bg-white">
                    <div className="input-group">
                        <textarea
                            className="form-control"
                            placeholder="Type your message here..."
                            value={input}
                            onChange={e => setInput(e.target.value)}
                            onKeyDown={handleKeyDown}
                            rows={1}
                            style={{ resize: 'none' }}
                        />
                        <button
                            className="btn btn-primary"
                            onClick={handleSubmit}
                            disabled={loading || !input.trim()}
                        >
                            {loading ? 'Sending...' : 'Send'}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}

export async function askLLM(question) {
    // const apiUrl = 'http://localhost:83/ai/chat'; // Flask API endpoint
    const apiUrl = '/ai/chat'; // Flask API endpoint

    try {
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question: question }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error('Error from API:', errorData);
            throw new Error(`API request failed with status ${response.status}: ${errorData.error || 'Unknown error'}`);
        }

        const data = await response.json();
        return data.answer;
    } catch (error) {
        console.error('Error sending request to API:', error);
        return null; // Or handle the error
        //  as needed in your component
    }
}


export function ChatLauncher() {
  const [open, setOpen] = useState(false);
  const wrapperRef = useRef(null);

  // collapse when clicking outside
  useEffect(() => {
    function handleClickOutside(event) {
      if (open && wrapperRef.current && !wrapperRef.current.contains(event.target)) {
        setOpen(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [open]);

  return (
    <div ref={wrapperRef}>
      {/* Always mounted, just hidden via CSS */}
      <div className={`chat-window ${open ? 'open' : ''}`}>
        <div className="d-flex justify-content-end p-2">
          <button
            type="button"
            className="btn-close"
            aria-label="Close"
            onClick={() => setOpen(false)}
          />
        </div>
        <div className="flex-grow-1 overflow-auto">
          <LLMConsole />
        </div>
      </div>

      {/* Launcher button, hidden when open */}
      <button
        type="button"
        className={`btn btn-primary chat-launcher-button rounded-circle d-flex align-items-center justify-content-center ${open ? 'd-none' : ''}`}
        onClick={() => setOpen(true)}
      >
        💬
      </button>
    </div>
  );
}
