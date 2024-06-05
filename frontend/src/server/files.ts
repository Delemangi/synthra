import type { FileMetadata } from '$lib/types/FileMetadata';
import type { FileUploaded } from '$lib/types/FileUploaded';
import axios from 'axios';

const BASE_URL = import.meta.env.VITE_BASE_URL;

export const getFilesForSpecifiedUser = async (accessToken: string) => {
  const result = await axios.get<FileMetadata[]>(`${BASE_URL}/files/`, {
    headers: {
      authorization: `Bearer ${accessToken}`
    }
  });

  return result.data;
};

export const getMetadataFilePath = async (path: string) => {
  const result = await axios.get<FileMetadata>(`${BASE_URL}/files/metadata/${path}/`);

  return result.data;
};

export const sendFileForSpecifiedUser = async (accessToken: string, file: File) => {
  const formData = new FormData();
  formData.append('file', file);

  const result = await axios.post<FileUploaded>(`${BASE_URL}/files/`, formData, {
    headers: {
      authorization: `Bearer ${accessToken}`
    }
  });

  return result.data;
};

export const getFileByPath = async (accessToken: string, path: string) => {
  const result = await axios.get(`${BASE_URL}/files/download/${path}/`, {
    responseType: 'blob',
    headers: {
      authorization: `Bearer ${accessToken}`
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
