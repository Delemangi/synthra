<script lang="ts">
  import type { FileMetadata } from '$lib/types/FileMetadata';
  import { Box, Button, Flex, Title, createStyles, type DefaultTheme } from '@svelteuidev/core';
  import { onMount } from 'svelte';
  import { getFileByPath, getMetadataFilePath } from '../../server/files';


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
  let file_url: string | null = null;

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
        file_url = URL.createObjectURL(retrievedFile);
      }
    } catch (error) {
      alert('The file does not exist, or has expired.');
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
      return;
    }

    try {
      if(file_url == null){
        throw Error()
      }
      const a = document.createElement('a');
      a.href = file_url;
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
        <p>File Name: {fileMetadata.name}</p>
        <p>File Size: {fileMetadata.size} bytes</p>
      </Box>
    {:else}
      <p>Loading...</p>
    {/if}

    <Button on:click={downloadFile}>Download</Button>
    <br/>
    {#if file_url}
      <div style="display: flex; justify-content: center; align-items: center; height: 80vh; width: 80vw; border: 2px solid #ccc;">
        <iframe src={file_url} frameborder="0" style="width: 100%; height: 100%; border: none;" title="File"></iframe>
    </div>
    {/if}
  </Flex>
</div>
