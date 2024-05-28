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
  import { deleteWebhookPost } from '../../../axios/axios-request';
  import { FileMetadata } from '../../types/FileMetadata';
  import { WebHook } from '$lib/types/WebHook';

  export let webhook: WebHook = new WebHook(
    0,"a","a"
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


  async function deleteWebhook(): Promise<void> {
    try {
      const confirmed = confirm('Are you sure you want to delete this webhook?');
      if (confirmed) {
        await deleteWebhookPost(localStorage.getItem('accessToken'), webhook.id);
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
      {webhook.id}
    </Text>
    <Text size="sm" css={{ flex: 1 }}>
      {webhook.platform}
    </Text>
    <Text size="sm" css={{ flex: 1 }}>
      {webhook.url}
    </Text>
    <Flex justify="left" gap="xs" css={{ flex: 1 }}>
      <Tooltip openDelay={10} label="Delete">
        <ActionIcon color="red" variant="filled" on:click={deleteWebhook}>
          <Trash size={20} />
        </ActionIcon>
      </Tooltip>
    </Flex>
  </Flex>
</Box>
