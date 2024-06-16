import { type AccessToken } from '$lib/types/AccessToken';
import axios from 'axios';

const BASE_URL = import.meta.env.VITE_BASE_URL;

export const getPermanentToken = async (accessToken: string) => {
  const result = await axios.post<AccessToken>(
    `${BASE_URL}/auth/get-sharex-token`,
    new FormData(),
    {
      headers: {
        authorization: `Bearer ${accessToken}`
      }
    }
  );

  return result.data;
};
