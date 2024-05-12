<script lang="ts">
  import FileRow from '$lib/components/user/FileRow.svelte';
  import TitleFileRow from '$lib/components/user/TitleFileRow.svelte';
  import type { FileMetadata } from '$lib/types/FileMetadata';
  import {
    Box,
    Button,
    Flex,
    Overlay,
    Title,
    createStyles,
    type DefaultTheme
  } from '@svelteuidev/core';
  import { onMount } from 'svelte';
  import { getFilesForSpecifiedUser, sendFileForSpecifiedUser } from '../../../axios/axios-request';

  let filesToUpload: FileList | null = null;

  async function sendData(): Promise<void> {
    if (filesToUpload != null) {
      console.log(filesToUpload);
      await sendFileForSpecifiedUser(localStorage.getItem('accessToken'), filesToUpload[0]);
      window.location.reload();
    } else {
      console.log('No file selected');
    }
  }
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

  let userFiles: FileMetadata[] = [];

  onMount(async function () {
    let accessToken = localStorage.getItem('accessToken');
    userFiles = await getFilesForSpecifiedUser(accessToken);
  });
  let visible = false;
</script>

<Button on:click={() => (visible = !visible)}>Upload file</Button>

<TitleFileRow />

{#each userFiles as file}
  <FileRow {file} />
{/each}

{#if visible}
  <Overlay opacity={0.9} color="#000" zIndex={5} center class={classes.flexOverlay}>
    <Box class={getStyles()}>
      <Flex direction="column" align="space-evenly" gap="md" justify="center">
        <Title order={3}>Upload your file</Title>

        <input type="file" id="myFile" name="filename" bind:files={filesToUpload} />

        <Flex justify="space-around" align="center">
          <Button variant="filled" on:click={async () => await sendData()}>Submit</Button>
          <Button variant="light" on:click={() => (visible = false)}>Close</Button>
        </Flex>
      </Flex>
    </Box>
  </Overlay>
{/if}
