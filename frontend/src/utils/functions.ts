import { SUPPORTED_FILE_TYPES } from './constants';

export const isFieldSuitable = (field: string) => field.length >= 5 && field.length <= 24;

export const isFileTypeSupported = (url: string | null) => {
  if (url == null) {
    return false;
  }

  const extension = url.slice(((url.lastIndexOf('.') - 1) >>> 0) + 2).toLowerCase();

  return SUPPORTED_FILE_TYPES.includes(`.${extension}`);
};

export const generateShareXTemplate = (token: string, baseUrl: string) => {
  return {
    Version: '16.1.0',
    Name: 'Synthra',
    DestinationType: 'ImageUploader, TextUploader, FileUploader',
    RequestMethod: 'POST',
    RequestURL: `${import.meta.env.VITE_BASE_URL}/files/`,
    Headers: {
      Authorization: `Bearer ${token}`
    },
    Body: 'MultipartFormData',
    FileFormName: 'file',
    URL: `${baseUrl}/download?file={json:filename}`
  } as const;
};
