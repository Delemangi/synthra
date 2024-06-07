import { logout } from '../server/auth';

export const clearSession = async (sendRequest = false) => {
  const accessToken = localStorage.getItem('accessToken');

  localStorage.removeItem('accessToken');
  localStorage.removeItem('username');

  if (!accessToken || !sendRequest) {
    return;
  }

  await logout(accessToken);
};
