import React, { useState } from 'react';
import UploadDocument from '../components/UploadDocument';
import DocumentList from '../components/DocumentList';
import ChatBox from '../components/ChatBox';

export default function Dashboard() {
  const [refreshKey, setRefreshKey] = useState(0);

  return (
    <div className="dashboard-layout">
      <header className="topbar">
        <h1>📄 DocuAI</h1>
        <p>Document Management &amp; AI Assistant</p>
      </header>

      <div className="content-grid">
        <aside className="left-panel">
          <UploadDocument onUploadSuccess={() => setRefreshKey((prev) => prev + 1)} />
          <DocumentList refreshKey={refreshKey} />
        </aside>

        <main className="right-panel">
          <ChatBox />
        </main>
      </div>
    </div>
  );
}
