import axios from 'axios';
import { useAuthStore } from '../store/auth';

export const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api'
});

apiClient.interceptors.request.use(config => {
  const token = useAuthStore.getState().accessToken;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
