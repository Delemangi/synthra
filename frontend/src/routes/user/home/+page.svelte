<script lang="ts">
  import FileRow from '$lib/components/user/FileRow.svelte';
  import TitleFileRow from '$lib/components/user/TitleFileRow.svelte';
  import type { FileMetadata } from '$lib/types/FileMetadata';
  import {
    Box,
    Button,
    Checkbox,
    Flex,
    Overlay,
    Text,
    TextInput,
    Title,
    createStyles,
    type DefaultTheme
  } from '@svelteuidev/core';
  import { isAxiosError } from 'axios';
  import { onMount } from 'svelte';
  import { clearSession } from '../../../auth/session';
  import { getFilesForSpecifiedUser, sendFileForSpecifiedUser } from '../../../server/files';
  import { getWebhooksForSpecifiedUser } from '../../../server/webhooks';

  let filesToUpload: FileList | null = null;
  let privateFile = true;
  let passwordLock = false;
  let filePassword = '';

  const sendData = async () => {
    const accessToken = localStorage.getItem('accessToken');

    if (!accessToken) {
      alert('You need to be logged in.');
      return;
    }

    if (!filesToUpload) {
      return;
    }

    try {
      await sendFileForSpecifiedUser(accessToken, filesToUpload[0], filePassword, privateFile);
      filePassword = '';
      window.location.reload();
    } catch (error) {
      if (!isAxiosError(error)) {
        alert('An unknown error occurred.');
        return;
      }

      alert('An error occurred while uploading the file.');
    }
  };

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
        padding: 20,
        borderRadius: '$md'
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
  let allowWebhooks = false;
  let visible = false;

  onMount(async () => {
    let accessToken = localStorage.getItem('accessToken');

    if (!accessToken) {
      window.location.href = '/auth/login';
      return;
    }

    try {
      userFiles = await getFilesForSpecifiedUser(accessToken);
      const webhooks = await getWebhooksForSpecifiedUser(accessToken);

      allowWebhooks = webhooks.length > 0;
    } catch (error) {
      if (!isAxiosError(error)) {
        alert('An unknown error occurred.');
        return;
      }

      if (error.response?.status === 401) {
        await clearSession();
        window.location.href = '/auth/login';
        return;
      }

      alert('An error occurred while fetching the files.');
    }
  });

  let fileName: string | null = null;

  const handleFileChange = () => {
    fileName = filesToUpload?.[0].name ?? null;
  };
</script>

<div
  style="display: flex; flex-direction: column; justify-content: center; align-items: center; margin-bottom: 2rem;"
>
  <Title order={1}>Files</Title>
</div>

<div
  style="display: flex; flex-direction: column; justify-content: center; align-items: center; margin-bottom: 2rem;"
>
  <Button on:click={() => (visible = !visible)}>Upload</Button>
</div>

<TitleFileRow />
{#each userFiles as file}
  <FileRow {file} {allowWebhooks} />
{/each}

{#if visible}
  <Overlay opacity={1} color="#000" zIndex={5} center class={classes.flexOverlay}>
    <Box class={getStyles()}>
      <Flex direction="column" align="space-evenly" gap="md" justify="center">
        <Title order={3}>Upload File</Title>

        <div class="file-upload-wrapper">
          <Flex direction="column" justify="center" gap="md">
            <label for="file-upload" class="custom-file-upload">
              <Text align="center">Choose File</Text>
            </label>
            <input
              id="file-upload"
              type="file"
              name="filename"
              bind:files={filesToUpload}
              on:change={handleFileChange}
            />
          </Flex>
          <br />
          <Text align="center">
            {#if filesToUpload}
              {fileName}
            {:else}
              No file selected
            {/if}
          </Text>
        </div>

        <Flex justify="center" align="center" gap="md">
          <Checkbox bind:checked={privateFile}></Checkbox>
          <Text>Private?</Text>
        </Flex>
        <Flex justify="center" align="center" gap="md">
          <Checkbox bind:checked={passwordLock} on:change={() => (filePassword = '')}></Checkbox>
          <Text>Encrypt?</Text>
        </Flex>
        <TextInput
          bind:value={filePassword}
          required={passwordLock}
          disabled={!passwordLock}
          placeholder="Password..."
          type="password"
          label="Password (at least 5 characters)"
        />
        <Flex justify="space-around" align="center">
          <Button
            variant="filled"
            on:click={sendData}
            disabled={!filesToUpload?.length ||
              (filesToUpload?.length && passwordLock && filePassword.length < 5)}
          >
            Submit
          </Button>
          <Button variant="light" on:click={() => (visible = false)}>Close</Button>
        </Flex>
      </Flex>
    </Box>
  </Overlay>
{/if}

<style>
  .file-upload-wrapper {
    position: relative;
    display: inline-block;
  }

  .custom-file-upload {
    display: inline-block;
    padding: 8px 12px;
    cursor: pointer;
    background-color: #007bff;
    color: white;
    border-radius: 4px;
    font-size: 14px;
    font-weight: bold;
    text-align: center;
  }

  #file-upload {
    position: absolute;
    left: 0;
    top: 0;
    opacity: 0;
    width: 100%;
    height: 100%;
    cursor: pointer;
  }

  .custom-file-upload:hover {
    background-color: #0056b3;
  }
</style>
