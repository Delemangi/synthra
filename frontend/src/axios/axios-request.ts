import type { FileMetadata } from '$lib/types/FileMetadata';
import type { FileUploaded } from '$lib/types/FileUploaded';
import axios from 'axios';

const BASE_URL = import.meta.env.VITE_BASE_URL;

export async function getFilesForSpecifiedUser(accessToken: string | null) {
  const result = await axios.get<FileMetadata[]>(`${BASE_URL}/files`, {
    headers: {
      authorization: `Bearer ${accessToken}`
    }
  });

  return result.data;
}

export async function sendFileForSpecifiedUser(accessToken: string | null, file: File) {
  const formData = new FormData();
  formData.append('file', file);

  const result = await axios.post<FileUploaded>(`${BASE_URL}/files`, formData, {
    headers: {
      authorization: `Bearer ${accessToken}`
    }
  });

  return result.data;
}

export async function getCertainFileByPath(accessToken: string | null, path: string) {
  const result = await axios.get<File>(`${BASE_URL}/files/${path}`, {
    headers: {
      responseType: 'blob',
      authorization: `Bearer ${accessToken}`
    }
  });

  return new File([result.data], path);
}

export async function deleteFileByPath(accessToken: string | null, path: string): Promise<void> {
  const result = await axios.delete(`${BASE_URL}/files/${path}`, {
    headers: {
      authorization: `Bearer ${accessToken}`
    }
  });

  return result.data;
}
