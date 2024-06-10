import type { FileMetadata } from '$lib/types/FileMetadata';
import type { FileUploaded } from '$lib/types/FileUploaded';
import axios from 'axios';

const BASE_URL = import.meta.env.VITE_BASE_URL;

export const getFilesForSpecifiedUser = async (accessToken: string) => {
  const result = await axios.get<FileMetadata[]>(`${BASE_URL}/files`, {
    headers: {
      authorization: `Bearer ${accessToken}`
    }
  });

  return result.data;
};

export const addShareForFile = async (username: string, file_id: string) => {
  await axios.post(
    `${BASE_URL}/shares/create`,
    JSON.stringify({ username: username, file_id: file_id }),
    {
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json'
      }
    }
  );
};

export const deleteShareForFile = async (share_id: string) => {
  await axios.delete(`${BASE_URL}/shares/delete/${share_id}`);
};

export const getMetadataFilePath = async (path: string) => {
  const result = await axios.get<FileMetadata>(`${BASE_URL}/files/metadata/${path}/`);

  return result.data;
};

// isShared is false by default (which means that everyone can see it)
export const sendFileForSpecifiedUser = async (
  accessToken: string,
  file: File,
  password: string = '',
  isShared: boolean = false,
) => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('password', password);
  formData.append('is_shared', isShared.toString());

  const result = await axios.post<FileUploaded>(`${BASE_URL}/files/`, formData, {
    headers: {
      authorization: `Bearer ${accessToken}`,
      'Content-Type': 'multipart/form-data',
    }
  });

  return result.data;
};

export const getFileByPath = async (accessToken: string | null, path: string, password: string | null = null) => {
  const result = await axios.get(`${BASE_URL}/files/download/${path}`, {
    responseType: 'blob',
    headers: {
      authorization: `Bearer ${accessToken}`,
      'Password': password,
    }
  });

  return new File([result.data], path, { type: result.data.type });
};

export const deleteFileByPath = async (accessToken: string, path: string) => {
  const result = await axios.delete(`${BASE_URL}/files/${path}/`, {
    headers: {
      authorization: `Bearer ${accessToken}`
    }
  });

  return result.data;
};
