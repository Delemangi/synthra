import type { AccessToken } from '$lib/types/AccessToken';
import type { Code2FA } from '$lib/types/Code2FA';
import type { UserMetadata } from '$lib/types/UserMetadata';
import axios from 'axios';

const BASE_URL = import.meta.env.VITE_BASE_URL;

export const login = async (username: string, password: string, code2FA: string | null) => {
  const formData = new FormData();

  formData.append('username', username);
  formData.append('password', password);
  formData.append('code_2fa', code2FA == null ? '' : code2FA);

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

export const logout = async (token: string) => {
  const result = await axios.post(`${BASE_URL}/auth/logout`, new FormData(), {
    headers: {
      authorization: `Bearer ${token}`
    }
  });

  return result;
};

export const get2FAToken = async (username: string, password: string) => {
  const formData = new FormData();

  formData.append('username', username);
  formData.append('password', password);

  const result = await axios.post<Code2FA>(`${BASE_URL}/auth/2fa`, formData);

  return result;
};

export const remove2FAToken = async (username: string, password: string) => {
  const formData = new FormData();

  formData.append('username', username);
  formData.append('password', password);

  const result = await axios.post<Code2FA>(`${BASE_URL}/auth/2fa/disable`, formData);

  return result;
};

export const getUserMetadata = async (token: string) => {
  const result = await axios.get<UserMetadata>(`${BASE_URL}/auth/fetch_user_data`, {
    headers: {
      authorization: `Bearer ${token}`
    }
  });

  return result;
};
