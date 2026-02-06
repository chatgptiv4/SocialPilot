import { apiClient } from './client';

export interface HealthStatus {
  database: string;
  redis: string;
}

export const fetchHealth = async (): Promise<HealthStatus> => {
  const response = await apiClient.get<HealthStatus>('/health');
  return response.data;
};
