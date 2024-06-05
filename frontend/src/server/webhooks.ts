import type { Webhook } from '$lib/types/Webhook';
import axios from 'axios';

const BASE_URL = import.meta.env.VITE_BASE_URL;

export const getWebhooksForSpecifiedUser = async (accessToken: string) => {
  const result = await axios.get<Webhook[]>(`${BASE_URL}/webhooks/user-webhooks/`, {
    headers: {
      authorization: `Bearer ${accessToken}`
    }
  });

  return result.data;
};

export const uploadWebhook = async (accessToken: string, platform: string, url: string) => {
  const result = await axios.post(
    `${BASE_URL}/webhooks/create/`,
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
};

export const sendWebhook = async (webhookId: string, fileId: string) => {
  const result = await axios.post(
    `${BASE_URL}/webhooks/send?webhook_id=${webhookId}&file_id=${fileId}/`
  );

  return result.data;
};

export const deleteWebhookPost = async (accessToken: string, id: string) => {
  const result = await axios.delete(`${BASE_URL}/webhooks/delete/${id}/`, {
    headers: {
      authorization: `Bearer ${accessToken}`
    }
  });

  return result.data;
};
