import type { AccessToken } from '$lib/types/AccessToken';
import axios from 'axios';

const BASE_URL = import.meta.env.VITE_BASE_URL;

export const login = async (username: string, password: string) => {
  const formData = new FormData();
  formData.append('username', username);
  formData.append('password', password);

  const result = await axios.post<AccessToken>(`${BASE_URL}/auth/login`, formData);

  return result;
};

export const register = async (username: string, password: string) => {
  const result = await axios.post(`${BASE_URL}/auth/register`, {
    username,
    password
  });

  return result;
};
