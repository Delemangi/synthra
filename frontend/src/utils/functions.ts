import { SUPPORTED_FILE_TYPES } from './constants';

export const isFieldSuitable = (field: string) => field.length >= 5 && field.length <= 24;

export const isFileTypeSupported = (url: string | null) => {
  if (url == null) {
    return false;
  }

  const extension = url.slice(((url.lastIndexOf('.') - 1) >>> 0) + 2).toLowerCase();

  return SUPPORTED_FILE_TYPES.includes(`.${extension}`);
};
