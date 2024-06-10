import { HomeScreenInfo } from '$lib/types/HomeScreenInfo';

export const HOME_SCREEN_ITEMS = [
  new HomeScreenInfo(
    'Upload your files',
    'Upload your files to Synthra and access them from anywhere.',
    'Upload',
    'light',
    'pink'
  ),
  new HomeScreenInfo(
    'Share your files',
    'Share your files with friends and family by sending them a link to your file.',
    'Share',
    'light',
    'blue'
  ),
  new HomeScreenInfo(
    'Webhooks support',
    'Post your uploaded images to platforms that support webhooks!',
    'Webhooks',
    'light',
    'green'
  ),
  new HomeScreenInfo(
    'File encryption',
    'Encrypt your files using a secure password',
    'Encryption',
    'light',
    'gray'
  ),
  new HomeScreenInfo(
    'Browser preview',
    'Preview the files in the browser',
    'Preview',
    'light',
    'orange'
  ),
  new HomeScreenInfo('ShareX support', 'Full ShareX support!', 'ShareX', 'light', 'cyan')
];

export const SUPPORTED_FILE_TYPES = ['.pdf', '.png', '.jpg', '.jpeg', '.mp4', '.mp3', '.txt'];
