import type { FileMetadata } from '$lib/types/FileMetadata';
import type { FileUploaded } from '$lib/types/FileUploaded';
import type { WebHook } from '$lib/types/WebHook';
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

export async function getWebhooksForSpecifiedUser(accessToken: string | null) {
  const result = await axios.get<WebHook[]>(`${BASE_URL}/webhooks/user-webhooks`, {
    headers: {
      authorization: `Bearer ${accessToken}`
    }
  });

  return result.data;
}

export async function uploadWebhook(accessToken: string | null, platform: string, url: string) {
  const result = await axios.post(
    `${BASE_URL}/webhooks/create`,
    JSON.stringify({ platform: platform, url: url }),
    {
      headers: {
        authorization: `Bearer ${accessToken}`,
        Accept: 'application/json',
        'Content-Type': 'application/json'
      }
    }
  );

  return result.data;
}

export async function sendWebhook(webhookId: string, fileId: string) {
  const result = await axios.post(
    `${BASE_URL}/webhooks/send?webhook_id=${webhookId}&file_id=${fileId}`
  );

  return result.data;
}

export async function deleteWebhookPost(accessToken: string | null, id: number) {
  const result = await axios.delete(`${BASE_URL}/webhooks/delete/${id}`, {
    headers: {
      authorization: `Bearer ${accessToken}`
    }
  });

  return result.data;
}

export async function getMetadataFilePath(path: string) {
  const result = await axios.get<FileMetadata>(`${BASE_URL}/files/metadata/${path}`);

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

export async function getDownloadFileLink(path: string) {
  const result = await axios.get(`${BASE_URL}/files/download-link/${path}`);

  return new File([result.data], path);
}

export async function deleteFileByPath(accessToken: string | null, path: string) {
  const result = await axios.delete(`${BASE_URL}/files/${path}`, {
    headers: {
      authorization: `Bearer ${accessToken}`
    }
  });

  return result.data;
}
