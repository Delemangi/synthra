<script lang="ts">
  import { onMount } from 'svelte';
  import { createStyles, Button, Box, Flex, Title, type DefaultTheme } from '@svelteuidev/core';
  import { getMetadataFilePath, getCertainFileByPath } from '../../axios/axios-request';

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

  let filePath: string = '';
  let fileMetadata: File | null = null;

  onMount(async () => {
    const urlParams = new URLSearchParams(window.location.search);
    filePath = urlParams.get('file');

    try {
      const response = await getMetadataFilePath(filePath);
      fileMetadata = response;
    } catch (error) {
      console.error('Error retrieving file metadata:', error);
      alert('File does not exist or is expired');
      document.location.href = '/';
    }
  });

  async function downloadFile(): Promise<void> {
    try {
      // eslint-disable-next-line no-undef
      let retrievedFile: void | globalThis.File = await getCertainFileByPath(
        localStorage.getItem('accessToken'),
        filePath
      );
      if (retrievedFile) {
        const url = URL.createObjectURL(retrievedFile);
        const a = document.createElement('a');
        a.href = url;
        a.download = filePath;
        a.click();
        URL.revokeObjectURL(url);
      }
    } catch (e) {
      console.error('Error downloading file:', e);
    }
  }
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
      <p>Loading file metadata...</p>
    {/if}

    <Button on:click={downloadFile}>Download</Button>
  </Flex>
</div>
