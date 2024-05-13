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
  import { Download, ExternalLink, EyeOpen, Trash } from 'radix-icons-svelte';
  import { deleteFileByPath, getCertainFileByPath } from '../../../axios/axios-request';
  import { FileMetadata } from '../../types/FileMetadata';

  export let file: FileMetadata = new FileMetadata(
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

  async function getFile(): Promise<void> {
    try {
      // eslint-disable-next-line no-undef
      let retrievedFile: void | globalThis.File = await getCertainFileByPath(
        localStorage.getItem('accessToken'),
        file.path
      );
      if (retrievedFile) {
        const url = URL.createObjectURL(retrievedFile);
        const a = document.createElement('a');
        a.href = url;
        a.download = file.name;
        a.click();
        URL.revokeObjectURL(url);
      }
    } catch (e) {
      console.log(e);
    }
  }

  function copyClipboard(): void {
    navigator.clipboard.writeText('http://localhost:3000/download/?file=' + file.path);
    alert('Successfully, copied the link to clipboard');
  }

  async function deleteFile(): Promise<void> {
    try {
      const confirmed = confirm('Are you sure you want to delete this file?');
      if (confirmed) {
        await deleteFileByPath(localStorage.getItem('accessToken'), file.path);
        window.location.reload();
      }
    } catch (e) {
      console.log(e);
    }
  }

  $: ({ getStyles } = useStyles());
</script>

<Box class={getStyles()}>
  <Flex align="center" justify="space-evenly" style="height: 100%;">
    <Text size="sm" css={{ flex: 1 }}>
      {file.name}
    </Text>
    <Text size="sm" css={{ flex: 1 }}>
      {file.encrypted}
    </Text>
    <Text size="sm" css={{ flex: 1 }}>
      {Math.round(file.size / 1024)}
    </Text>
    <Text size="sm" css={{ flex: 1 }}>
      {file.timestamp}
    </Text>
    <Text size="sm" css={{ flex: 1 }}>
      {file.expiration}
    </Text>
    <Flex justify="left" gap="xs" css={{ flex: 1 }}>
      <Tooltip openDelay={10} label="Preview">
        <ActionIcon variant="filled" color="blue">
          <EyeOpen size={20} />
        </ActionIcon>
      </Tooltip>
      <Tooltip openDelay={10} label="Share">
        <ActionIcon variant="filled" color="cyan" on:click={copyClipboard}>
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
