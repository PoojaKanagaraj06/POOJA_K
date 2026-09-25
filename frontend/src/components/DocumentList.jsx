import React, { useEffect, useState } from 'react';
import { deleteDocument, downloadDocument, getDocuments } from '../services/api';

export default function DocumentList({ refreshKey }) {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const fetchDocuments = async () => {
    try {
      setLoading(true);
      const data = await getDocuments();
      setDocuments(data);
      setError('');
    } catch (err) {
      setError('Unable to load documents.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, [refreshKey]);

  const handleDownload = async (doc) => {
    try {
      const blob = await downloadDocument(doc.id);
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = doc.originalName;
      link.click();
      URL.revokeObjectURL(url);
    } catch (err) {
      setError('Download failed.');
    }
  };

  const handleDelete = async (docId) => {
    try {
      await deleteDocument(docId);
      fetchDocuments();
    } catch (err) {
      setError(err?.response?.data?.detail || 'Delete failed.');
    }
  };

  return (
    <div className="card documents-panel">
      <h3>Documents</h3>
      {loading ? <p>Loading documents...</p> : error ? <p className="error-text">{error}</p> : documents.length === 0 ? <p>No documents uploaded yet.</p> : (
        <div className="document-list">
          {documents.map((doc) => (
            <div className="document-item" key={doc.id}>
              <div className="document-meta">
                <span className="doc-icon">📄</span>
                <div>
                  <strong>{doc.originalName}</strong>
                  <p>{doc.fileType} • {doc.fileSize} bytes</p>
                  <small>{new Date(doc.uploadedAt).toLocaleString()}</small>
                </div>
              </div>
              <div className="actions">
                <button className="secondary-button" onClick={() => handleDownload(doc)}>Download</button>
                <button className="danger-button" onClick={() => handleDelete(doc.id)}>Delete</button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
