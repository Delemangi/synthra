import type { AccessToken } from '$lib/types/AccessToken';
import type { TokenValidity } from '$lib/types/TokenValidity';
import axios from 'axios';

const BASE_URL = import.meta.env.VITE_BASE_URL;

export const login = async (username: string, password: string) => {
  const formData = new FormData();
  formData.append('username', username);
  formData.append('password', password);

  const result = await axios.post<AccessToken>(`${BASE_URL}/auth/login/`, formData);

  return result;
};

export const register = async (username: string, password: string) => {
  const formData = new FormData();
  formData.append('username', username);
  formData.append('password', password);

  const result = await axios.post<AccessToken>(`${BASE_URL}/auth/register/`, formData);

  return result;
};

export const validate = async (token: string) => {
  const result = await axios.post<TokenValidity>(`${BASE_URL}/auth/validate/`, {
    token
  });

  return result;
};
