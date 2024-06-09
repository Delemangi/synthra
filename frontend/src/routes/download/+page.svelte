<script lang="ts">
  import type { FileMetadata } from '$lib/types/FileMetadata';
  import {
    Box,
    Button,
    Flex,
    Text,
    Title,
    createStyles,
    type DefaultTheme
  } from '@svelteuidev/core';
  import { onMount } from 'svelte';
  import { getFileByPath, getMetadataFilePath } from '../../server/files';
  import { SUPPORTED_FILE_TYPES } from '../../utils/constants';
  import { isFileTypeSupported } from '../../utils/functions';

  const useStyles = createStyles((theme: DefaultTheme) => {
    return {
      root: {
        [`${theme.dark} &`]: {
          bc: theme.fn.themeColor('dark', 5),
          color: 'white'
        },
        height: '100%',
        backgroundColor: theme.fn.themeColor('gray', 1),
        opacity: 1,
        padding: 20
      },
      flexOverlay: {
        display: 'flex',
        height: '100%',
        justifyContent: 'center',
        alignItems: 'center',
        direction: 'column',
        backdropFilter: 'blur(5px)'
      }
    };
  });

  $: ({ classes, getStyles } = useStyles());

  let filePath: string | null = null;
  let fileMetadata: FileMetadata | null = null;
  let fileUrl: string | null = null;

  onMount(async () => {
    const urlParams = new URLSearchParams(window.location.search);
    filePath = urlParams.get('file');

    if (!filePath) {
      return;
    }

    try {
      fileMetadata = await getMetadataFilePath(filePath);
      const accessToken = localStorage.getItem('accessToken');

      if (!accessToken) {
        alert('You need to be logged in.');
        return;
      }

      let retrievedFile = await getFileByPath(accessToken, filePath);

      if (retrievedFile) {
        fileUrl = URL.createObjectURL(retrievedFile);
      }
    } catch (error) {
      alert('The file does not exist, or has expired.');
      window.location.href = '/';
    }
  });

  const downloadFile = async () => {
    if (!filePath) {
      alert('An error occurred while downloading the file.');
      return;
    }

    const accessToken = localStorage.getItem('accessToken');

    if (!accessToken) {
      alert('You need to be logged in.');
      window.location.href = '/';
      return;
    }

    try {
      if (fileUrl == null) {
        throw Error();
      }

      const a = document.createElement('a');

      a.href = fileUrl;
      a.download = filePath;

      // Firefox fix
      document.body.appendChild(a);

      a.click();

      // Firefox fix
      document.body.removeChild(a);
    } catch {
      alert('An error occurred while downloading the file.');
    }
  };
</script>

<div class={classes.root}>
  <Flex direction="column" align="center">
    <Title order={3}>Download File</Title>

    {#if fileMetadata}
      <Box class={getStyles()}>
        <Text>File Name: {fileMetadata.name}</Text>
        <Text>File Size: {fileMetadata.size} bytes</Text>
      </Box>
    {:else}
      <Text>Loading...</Text>
    {/if}

    <Button on:click={downloadFile}>Download</Button>
    <br />
    {#if fileUrl && isFileTypeSupported(filePath)}
      <div
        style="display: flex; justify-content: center; align-items: center; height: 80vh; width: 80vw; border: 2px solid #ccc;"
      >
        <iframe
          src={fileUrl}
          frameborder="0"
          style="width: 100%; height: 100%; border: none;"
          title="File"
        ></iframe>
      </div>
    {:else}
      <div style="text-align: center;">
        <Text>
          The file must be one of the following types to be previewed: {SUPPORTED_FILE_TYPES.join(
            ', '
          )}
        </Text>
      </div>
    {/if}
  </Flex>
</div>
