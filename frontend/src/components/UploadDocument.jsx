import React, { useState } from 'react';
import { uploadDocument } from '../services/api';

export default function UploadDocument({ onUploadSuccess }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async () => {
    if (!selectedFile) {
      setError('Please choose a file to upload.');
      return;
    }

    try {
      setIsUploading(true);
      setError('');
      await uploadDocument(selectedFile);
      setSelectedFile(null);
      onUploadSuccess();
    } catch (err) {
      setError(err?.response?.data?.detail || 'Upload failed.');
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="card upload-panel">
      <h3>Upload Document</h3>
      <label className="file-input-wrap">
        <input type="file" accept=".txt,.md,.json" onChange={(e) => setSelectedFile(e.target.files[0])} />
        <span>{selectedFile ? selectedFile.name : 'Choose a file'}</span>
      </label>
      {error && <p className="error-text">{error}</p>}
      <button className="primary-button" onClick={handleSubmit} disabled={isUploading || !selectedFile}>
        {isUploading ? 'Uploading...' : 'Upload Document'}
      </button>
    </div>
  );
}
