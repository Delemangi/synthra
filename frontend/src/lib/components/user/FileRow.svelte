<script lang="ts">
  import {
    ActionIcon,
    Box,
    Button,
    Flex,
    Overlay,
    Text,
    TextInput,
    Title,
    Tooltip,
    createStyles,
    type theme
  } from '@svelteuidev/core';
  import { isAxiosError } from 'axios';
  import { DoubleArrowRight, Download, ExternalLink, EyeOpen, Trash } from 'radix-icons-svelte';
  import {
    addShareForFile,
    deleteFileByPath,
    deleteShareForFile,
    getFileByPath
  } from '../../../server/files';
  import { getWebhooksForSpecifiedUser, sendWebhook } from '../../../server/webhooks';
  import { FileMetadata } from '../../types/FileMetadata';

  export let file = new FileMetadata(
    'test',
    'test',
    1,
    'test',
    'test',
    [],
    new Date(2021, 1, 1),
    new Date(2021, 1, 1),
    'test'
  );

  export let allowWebhooks: boolean;

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

  const downloadFile = () => {
    if (file.encrypted) isDownloadWindowVisible = true;
    else getFile();
  };

  const getFile = async () => {
    const accessToken = localStorage.getItem('accessToken');

    if (!accessToken) {
      alert('You need to be logged in.');

      return;
    }

    try {
      let [retrievedFile] = await getFileByPath(accessToken, file.path, downloadFilePassword);

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

        isDownloadWindowVisible = false;
      }
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

  let shareTooltipText = 'Share';
  let visible = false;
  let usernameShare = '';
  let isDownloadWindowVisible = false;
  let downloadFilePassword = '';

  const copyToClipboard = () => {
    const baseUrl = window.location.origin;
    navigator.clipboard.writeText(`${baseUrl}/download/?file=${file.path}`);

    shareTooltipText = 'Copied!';

    setTimeout(() => {
      shareTooltipText = 'Share';
    }, 2000);
  };

  const resetTooltipText = () => {
    shareTooltipText = 'Share';
  };

  const preview = () => {
    const baseUrl = window.location.origin;
    const location = `${baseUrl}/download/?file=${file.path}`;
    window.location.href = location;
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

  const shareFile = async () => {
    try {
      await addShareForFile(usernameShare, file.id);
      window.location.reload();
    } catch (error) {
      if (!isAxiosError(error)) {
        alert('An unknown error occurred.');
        return;
      }

      if (error.response?.status === 404) {
        alert('That user does not exist.');
        return;
      }

      alert('An error occurred while sharing the file.');
    }
  };

  const deleteShare = async (id: string) => {
    await deleteShareForFile(id);
    window.location.reload();
  };

  const openShare = () => {
    if (file.shared) {
      visible = true;
    }
  };

  const dateTimeFormat = new Intl.DateTimeFormat('en-UK', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: 'numeric',
    minute: 'numeric'
  });

  $: ({ classes, getStyles } = useStyles());
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
    {#if file.shared}
      <Text
        size="sm"
        css={{ flex: 1, textAlign: 'center', textDecoration: 'underline', cursor: 'pointer' }}
        on:click={openShare}
      >
        Manage Sharing ({file.shared_people.length})
      </Text>
    {:else}
      <Text size="sm" css={{ flex: 1, textAlign: 'center' }}>Public</Text>
    {/if}
    <Text size="sm" css={{ flex: 1, textAlign: 'center' }}>
      {dateTimeFormat.format(new Date(file.timestamp))}
    </Text>
    <Text size="sm" css={{ flex: 1, textAlign: 'center' }}>
      {dateTimeFormat.format(new Date(file.expiration))}
    </Text>
    <Flex justify="center" gap="xs" css={{ flex: 1 }}>
      <Tooltip openDelay={10} label="Send to Webhook">
        <ActionIcon
          variant="filled"
          color="blue"
          on:click={sendToWebHooks}
          disabled={!allowWebhooks}
        >
          <DoubleArrowRight size={20} />
        </ActionIcon>
      </Tooltip>
      <Tooltip openDelay={10} label="Preview">
        <ActionIcon variant="filled" color="blue" on:click={preview}>
          <EyeOpen size={20} />
        </ActionIcon>
      </Tooltip>
      <Tooltip openDelay={10} label={shareTooltipText}>
        <ActionIcon
          variant="filled"
          color="cyan"
          on:click={copyToClipboard}
          on:mouseleave={resetTooltipText}
        >
          <ExternalLink size={20} />
        </ActionIcon>
      </Tooltip>
      <Tooltip openDelay={10} label="Download">
        <ActionIcon variant="filled" on:click={downloadFile}>
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

{#if visible}
  <Overlay opacity={1} color="#000" zIndex={5} center class={classes.flexOverlay}>
    <Box class={getStyles()}>
      <Flex direction="column" align="space-evenly" gap="md" justify="center">
        <Title order={3}>Share File</Title>
        {#if file.shared_people.length > 0}
          {#each file.shared_people as share}
            <Box class={getStyles()}>
              <Flex align="center" justify="space-evenly" style="height: 100%;">
                <Text size="sm" css={{ flex: 1, textAlign: 'center' }}>
                  {share.username}
                </Text>
                <Tooltip openDelay={10} label="Delete">
                  <ActionIcon color="red" variant="filled" on:click={() => deleteShare(share.id)}>
                    <Trash size={20} />
                  </ActionIcon>
                </Tooltip>
              </Flex>
            </Box>
          {/each}
        {:else}
          <Text>This file is not yet shared with anyone.</Text>
        {/if}
        <br />
        <Flex justify="space-around" align="center">
          <TextInput label="Username" bind:value={usernameShare} />
        </Flex>
        <Flex justify="space-around" align="center">
          <Button variant="filled" on:click={shareFile}>Share</Button>
        </Flex>
        <br />
        <Flex justify="space-around" align="center">
          <Button variant="light" on:click={() => (visible = false)}>Close</Button>
        </Flex>
      </Flex>
    </Box>
  </Overlay>
{/if}

{#if isDownloadWindowVisible}
  <Overlay opacity={0.9} color="#000" zIndex={5} center class={classes.flexOverlay}>
    <Box class={getStyles()}>
      <Flex direction="column" align="space-evenly" gap="l" justify="center">
        <Title order={3}>Download File</Title>
        <TextInput
          type="password"
          name="filepassword"
          bind:value={downloadFilePassword}
          placeholder="Password..."
        />
        <Flex gap="lg" justify="space-between">
          <Button variant="filled" on:click={getFile} disabled={!downloadFilePassword?.length}>
            Submit
          </Button>
          <Button variant="light" on:click={() => (isDownloadWindowVisible = false)}>Close</Button>
        </Flex>
      </Flex>
    </Box>
  </Overlay>
{/if}
