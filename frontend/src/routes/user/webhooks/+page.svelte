<script lang="ts">
  import WebhookRow from '$lib/components/user/WebhookRow.svelte';
  import TitleWebhookRow from '$lib/components/user/TitleWebhookRow.svelte';
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
  import { getWebhooksForSpecifiedUser, uploadWebhook } from '../../../axios/axios-request';
  import type { WebHook } from '$lib/types/WebHook';

  let platform: string = '';
  let url: string = '';
  async function sendData(): Promise<void> {
    await uploadWebhook(localStorage.getItem('accessToken'), platform, url);
    window.location.reload();
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

  let userWebhooks: WebHook[] = [];

  onMount(async function () {
    let accessToken = localStorage.getItem('accessToken');
    userWebhooks = await getWebhooksForSpecifiedUser(accessToken);
    console.log(userWebhooks);
  });
  let visible = false;
</script>

<Button on:click={() => (visible = !visible)}>Add webhook</Button>

<TitleWebhookRow />

{#each userWebhooks as webhook}
  <WebhookRow {webhook} />
{/each}

{#if visible}
  <Overlay opacity={0.9} color="#000" zIndex={5} center class={classes.flexOverlay}>
    <Box class={getStyles()}>
      <Flex direction="column" align="space-evenly" gap="md" justify="center">
        <Title order={3}>Add webhook</Title>

        Platform
        <input id="platform" name="platform" bind:value={platform} />

        Url
        <input id="url" name="url" bind:value={url} />

        <Flex justify="space-around" align="center">
          <Button variant="filled" on:click={async () => await sendData()}>Submit</Button>
          <Button variant="light" on:click={() => (visible = false)}>Close</Button>
        </Flex>
      </Flex>
    </Box>
  </Overlay>
{/if}
