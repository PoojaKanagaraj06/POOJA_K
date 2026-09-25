import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
});

export const uploadDocument = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  const response = await api.post('/api/documents/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return response.data;
};

export const getDocuments = async () => {
  const response = await api.get('/api/documents');
  return response.data;
};

export const downloadDocument = async (documentId) => {
  const response = await api.get(`/api/documents/${documentId}/download`, {
    responseType: 'blob',
  });
  return response.data;
};

export const deleteDocument = async (documentId) => {
  const response = await api.delete(`/api/documents/${documentId}`);
  return response.data;
};

export const askQuestion = async (question) => {
  const response = await api.post('/api/chat', { question });
  return response.data;
};

export default api;
