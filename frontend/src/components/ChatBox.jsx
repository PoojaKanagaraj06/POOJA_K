import React, { useState } from 'react';
import { askQuestion } from '../services/api';

export default function ChatBox() {
  const [question, setQuestion] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    const trimmedQuestion = question.trim();
    if (!trimmedQuestion) {
      setError('Please enter a question.');
      return;
    }

    setChatHistory((prev) => [...prev, { role: 'user', text: trimmedQuestion }]);
    setQuestion('');
    setError('');
    setLoading(true);

    try {
      const response = await askQuestion(trimmedQuestion);
      setChatHistory((prev) => [...prev, { role: 'assistant', text: response.answer, sources: response.sources || [] }]);
    } catch (err) {
      setError(err?.response?.data?.detail || 'Unable to get a response.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card chat-panel">
      <h3>AI Assistant</h3>
      <div className="chat-thread">
        {chatHistory.length === 0 ? (
          <p className="empty-chat">Ask questions about your uploaded documents.</p>
        ) : (
          chatHistory.map((entry, index) => (
            <div key={index} className={`message ${entry.role}`}>
              <div className="bubble">
                <strong>{entry.role === 'user' ? 'You:' : 'AI:'}</strong>
                <p>{entry.text}</p>
                {entry.sources && entry.sources.length > 0 && (
                  <div className="source-list">
                    {entry.sources.map((source) => (
                      <span key={source.id} className="source-badge">📄 {source.originalName}</span>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))
        )}
      </div>
      {error && <p className="error-text">{error}</p>}
      <form onSubmit={handleSubmit} className="chat-form">
        <textarea value={question} onChange={(e) => setQuestion(e.target.value)} rows={4} placeholder="Ask a question..." />
        <button type="submit" className="primary-button" disabled={loading}>{loading ? 'Thinking...' : 'Ask'}</button>
      </form>
    </div>
  );
}
