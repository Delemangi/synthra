export const clearSession = () => {
  localStorage.removeItem('accessToken');
  localStorage.removeItem('username');
};
