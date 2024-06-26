<script lang="ts">
  import type { FileMetadata } from '$lib/types/FileMetadata';
  import {
    Box,
    Button,
    Flex,
    Text,
    TextInput,
    Title,
    createStyles,
    type DefaultTheme
  } from '@svelteuidev/core';
  import { isAxiosError } from 'axios';
  import { onMount } from 'svelte';
  import { getFileByPath, getMetadataFilePath } from '../../server/files';
  import { SUPPORTED_FILE_TYPES } from '../../utils/constants';

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
  let downloadFilePassword: string = '';
  let isPreviewable: boolean = false;
  let isImage: boolean = false;

  onMount(async () => {
    const urlParams = new URLSearchParams(window.location.search);
    filePath = urlParams.get('file');

    if (!filePath) {
      return;
    }

    try {
      fileMetadata = await getMetadataFilePath(filePath);
      const accessToken = localStorage.getItem('accessToken');

      let [retrievedFile, contentType] = await getFileByPath(
        localStorage.getItem('accessToken'),
        filePath,
        downloadFilePassword
      );

      isPreviewable = contentType != 'application/octet-stream';
      isImage = contentType.startsWith('image/');

      fileUrl = window.URL.createObjectURL(retrievedFile);

      if (!accessToken) {
        alert('You need to be logged in.');
        return;
      }
    } catch (error) {
      alert('The file does not exist, or has expired.');
      window.location.href = '/';
    }
  });

  const downloadFile = async () => {
    if (filePath == null) {
      alert('An error occurred while downloading the file.');
      return;
    }

    try {
      let [retrievedFile] = await getFileByPath(
        localStorage.getItem('accessToken'),
        filePath,
        downloadFilePassword
      );

      if (retrievedFile) {
        fileUrl = URL.createObjectURL(retrievedFile);
      }

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
    } catch (error) {
      if (!isAxiosError(error)) {
        alert('An unknown error occurred.');
        return;
      }

      if (error.response?.status === 404) {
        alert('That file does not exist.');
        return;
      }

      if (error.response?.status === 403) {
        alert('Invalid password.');
        return;
      }

      alert('An error occurred while downloading the file.');
    }
  };
</script>

<div class={classes.root}>
  <Flex direction="column" align="center" justify="space-around">
    <Title order={3}>Download File</Title>

    {#if fileMetadata}
      <Box class={getStyles()}>
        <Text>File Name: {fileMetadata.name}</Text>
        <Text>File Size: {fileMetadata.size} bytes</Text>
        <Text>File Author: {fileMetadata.author}</Text>
      </Box>
    {:else}
      <Text>Loading...</Text>
    {/if}

    {#if fileMetadata?.encrypted}
      <TextInput
        placeholder="Password..."
        type="password"
        bind:value={downloadFilePassword}
        required
      />
      <br />
    {/if}

    <Button
      on:click={downloadFile}
      disabled={fileMetadata?.encrypted && !downloadFilePassword?.length}
    >
      Download
    </Button>

    <br />

    {#if fileUrl && isPreviewable}
      <div
        style="display: flex; justify-content: center; align-items: center; height: 80vh; width: 80vw;"
      >
        {#if isImage}
          <img
            src={fileUrl}
            alt="preview"
            style="max-width: 100%; max-height: 100%; object-fit: contain;"
          />
        {:else}
          <iframe
            src={fileUrl}
            frameborder="0"
            style="width: 100%; height: 100%; border: 2px solid #ccc;"
            title="File"
          ></iframe>
        {/if}
      </div>
    {:else}
      <div style="text-align: center;">
        <Text>
          The file must be one of the following types to be previewed: {SUPPORTED_FILE_TYPES.join(
            ', '
          )}.
        </Text>
      </div>
    {/if}
  </Flex>
</div>
