import axios from 'axios';

const BASE_URL = import.meta.env.VITE_BASE_URL;

export async function getFilesForSpecifiedUser(accessToken: string | null): Promise<File[]> {
  return await axios
    .get(`${BASE_URL}/files`, {
      headers: {
        authorization: `Bearer ${accessToken}`
      }
    })
    .then((response) => {
      return response.data;
    })
    .catch((error) => {
      console.log(error);
    });
}

export async function sendFileForSpecifiedUser(
  accessToken: string | null,
  file: File
): Promise<void> {
  const formData = new FormData();
  formData.append('file', file);

  await axios
    .post(`${BASE_URL}/files`, formData, {
      headers: {
        authorization: `Bearer ${accessToken}`
      }
    })
    .then((response) => {
      console.log(response);
    })
    .catch((error) => {
      console.log(error);
    });
}

export async function getCertainFileByPath(
  accessToken: string | null,
  path: string
): Promise<void | File> {
  return await axios
    .get(`${BASE_URL}/files/download/${path}`, {
      responseType: 'blob',
      headers: {
        authorization: `Bearer ${accessToken}`
      }
    })
    .then((response) => {
      const file = new File([response.data], path);
      return file;
    })
    .catch((error) => {
      console.log(error);
      throw error;
    });
}

export async function deleteFileByPath(accessToken: string | null, path: string): Promise<void> {
  await axios
    .delete(`${BASE_URL}/files/${path}`, {
      headers: {
        authorization: `Bearer ${accessToken}`
      }
    })
    .then((response) => {
      console.log(response);
    })
    .catch((error) => {
      console.log(error);
    });
}
