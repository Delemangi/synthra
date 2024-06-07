<script lang="ts">
  import TitleWebhookRow from '$lib/components/user/TitleWebhookRow.svelte';
  import WebhookRow from '$lib/components/user/WebhookRow.svelte';
  import type { Webhook } from '$lib/types/Webhook';
  import {
    Box,
    Button,
    Flex,
    Overlay,
    Title,
    createStyles,
    type DefaultTheme
  } from '@svelteuidev/core';
  import { isAxiosError } from 'axios';
  import { onMount } from 'svelte';
  import { clearSession } from '../../../auth/session';
  import { getWebhooksForSpecifiedUser, uploadWebhook } from '../../../server/webhooks';

  let name = '';
  let url = '';

  const sendData = async () => {
    const accessToken = localStorage.getItem('accessToken');

    if (!accessToken) {
      alert('You need to be logged in.');
      return;
    }

    await uploadWebhook(accessToken, name, url);
    window.location.reload();
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

  let userWebhooks: Webhook[] = [];
  let visible = false;

  onMount(async () => {
    let accessToken = localStorage.getItem('accessToken');

    if (!accessToken) {
      window.location.href = '/auth/login';
      return;
    }

    try {
      userWebhooks = await getWebhooksForSpecifiedUser(accessToken);
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

      alert('An error occurred while fetching the webhooks.');
    }
  });

  const URL_REGEX = /^(https?|ftp):\/\/[^\s/$.?#].[^\s]*$/i;
</script>

<div
  style="display: flex; flex-direction: column; justify-content: center; align-items: center; margin-bottom: 2rem;"
>
  <Title order={1}>Webhooks</Title>
</div>

<div
  style="display: flex; flex-direction: column; justify-content: center; align-items: center; margin-bottom: 2rem;"
>
  <Button on:click={() => (visible = !visible)}>Create</Button>
</div>

<TitleWebhookRow />

{#each userWebhooks as webhook}
  <WebhookRow {webhook} />
{/each}

{#if visible}
  <Overlay opacity={0.9} color="#000" zIndex={5} center class={classes.flexOverlay}>
    <Box class={getStyles()}>
      <Flex direction="column" align="space-evenly" gap="md" justify="center">
        <Title order={3}>Add Webhook</Title>

        Name
        <input bind:value={name} />

        URL
        <input bind:value={url} />

        <Flex justify="space-around" align="center">
          <Button
            variant="filled"
            on:click={sendData}
            disabled={!name || !url || !URL_REGEX.test(url)}
          >
            Submit
          </Button>
          <Button variant="light" on:click={() => (visible = false)}>Close</Button>
        </Flex>
      </Flex>
    </Box>
  </Overlay>
{/if}
