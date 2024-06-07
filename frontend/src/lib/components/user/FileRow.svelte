<script lang="ts">
  import {
    ActionIcon,
    Box,
    Flex,
    Text,
    Tooltip,
    createStyles,
    type theme
  } from '@svelteuidev/core';
  import { DoubleArrowRight, Download, ExternalLink, EyeOpen, Trash } from 'radix-icons-svelte';
  import { deleteFileByPath, getFileByPath } from '../../../server/files';
  import { getWebhooksForSpecifiedUser, sendWebhook } from '../../../server/webhooks';
  import { FileMetadata } from '../../types/FileMetadata';

  export let file = new FileMetadata(
    'test',
    'test',
    1,
    'test',
    new Date(2021, 1, 1),
    new Date(2021, 1, 1),
    'test'
  );

  const useStyles = createStyles((theme: theme) => {
    return {
      root: {
        [`${theme.dark} &`]: {
          bc: theme.fn.themeColor('dark', 5),
          color: 'white'
        },
        backgroundColor: '$gray50',
        textAlign: 'center',
        padding: '$10',
        borderRadius: '$md',
        '&:hover': {
          backgroundColor: '$gray100'
        }
      }
    };
  });

  const getFile = async () => {
    const accessToken = localStorage.getItem('accessToken');

    if (!accessToken) {
      alert('You need to be logged in.');

      return;
    }

    try {
      let retrievedFile = await getFileByPath(accessToken, file.path);

      if (retrievedFile) {
        const url = URL.createObjectURL(retrievedFile);
        const a = document.createElement('a');
        a.href = url;
        a.download = file.name;

        // Firefox fix
        document.body.appendChild(a);

        a.click();

        // Firefox fix
        document.body.removeChild(a);

        URL.revokeObjectURL(url);
      }
    } catch {
      alert('An error occurred while downloading the file.');
    }
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText(`${import.meta.env.VITE_BASE_URL}/download/?file=${file.path}`);
  };

  const sendToWebHooks = async () => {
    const accessToken = localStorage.getItem('accessToken');

    if (!accessToken) {
      alert('You need to be logged in.');

      return;
    }

    const webhooks = await getWebhooksForSpecifiedUser(accessToken);
    const promises = webhooks.map((webhook) => sendWebhook(webhook.id, file.id));

    await Promise.all(promises);
  };

  const deleteFile = async () => {
    const accessToken = localStorage.getItem('accessToken');

    if (!accessToken) {
      alert('You need to be logged in.');

      return;
    }

    const confirmation = confirm('Are you sure you want to delete this file?');

    if (confirmation) {
      await deleteFileByPath(accessToken, file.path);
      window.location.reload();
    }
  };

  const dateTimeFormat = new Intl.DateTimeFormat('en-UK', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: 'numeric',
    minute: 'numeric'
  });

  $: ({ getStyles } = useStyles());
</script>

<Box class={getStyles()}>
  <Flex align="center" justify="space-evenly" style="height: 100%;">
    <Text size="sm" css={{ flex: 1, textAlign: 'center' }}>
      {file.name}
    </Text>
    <Text size="sm" css={{ flex: 1, textAlign: 'center' }}>
      {(file.size / 1000).toFixed(2)}
    </Text>
    <Text size="sm" css={{ flex: 1, textAlign: 'center' }}>
      {file.encrypted ? 'Yes' : 'No'}
    </Text>
    <Text size="sm" css={{ flex: 1, textAlign: 'center' }}>
      {dateTimeFormat.format(new Date(file.timestamp))}
    </Text>
    <Text size="sm" css={{ flex: 1, textAlign: 'center' }}>
      {dateTimeFormat.format(new Date(file.expiration))}
    </Text>
    <Flex justify="center" gap="xs" css={{ flex: 1 }}>
      <Tooltip openDelay={10} label="Send to Webhook">
        <ActionIcon variant="filled" color="blue" on:click={sendToWebHooks}>
          <DoubleArrowRight size={20} />
        </ActionIcon>
      </Tooltip>
      <Tooltip openDelay={10} label="Preview">
        <ActionIcon variant="filled" color="blue">
          <EyeOpen size={20} />
        </ActionIcon>
      </Tooltip>
      <Tooltip openDelay={10} label="Share">
        <ActionIcon variant="filled" color="cyan" on:click={copyToClipboard}>
          <ExternalLink size={20} />
        </ActionIcon>
      </Tooltip>
      <Tooltip openDelay={10} label="Download">
        <ActionIcon variant="filled" on:click={getFile}>
          <Download size={20} />
        </ActionIcon>
      </Tooltip>
      <Tooltip openDelay={10} label="Delete">
        <ActionIcon color="red" variant="filled" on:click={deleteFile}>
          <Trash size={20} />
        </ActionIcon>
      </Tooltip>
    </Flex>
  </Flex>
</Box>
