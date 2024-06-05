<script lang="ts">
  import { Webhook } from '$lib/types/Webhook';
  import {
    ActionIcon,
    Box,
    Flex,
    Text,
    Tooltip,
    createStyles,
    type theme
  } from '@svelteuidev/core';
  import { Trash } from 'radix-icons-svelte';
  import { deleteWebhookPost } from '../../../server/webhooks';

  export let webhook = new Webhook('0', 'a', 'a');

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

  const deleteWebhook = async () => {
    const accessToken = localStorage.getItem('accessToken');

    if (!accessToken) {
      alert('You need to be logged in.');

      return;
    }

    try {
      const confirmation = confirm('Are you sure you want to delete this webhook?');

      if (confirmation) {
        await deleteWebhookPost(accessToken, webhook.id);
        window.location.reload();
      }
    } catch {
      alert('An error occurred while deleting the webhook.');
    }
  };

  $: ({ getStyles } = useStyles());
</script>

<Box class={getStyles()}>
  <Flex align="center" justify="space-evenly" style="height: 100%;">
    <Text size="sm" css={{ flex: 1, textAlign: 'center' }}>
      {webhook.platform}
    </Text>
    <Text size="sm" css={{ flex: 1, textAlign: 'center' }}>
      {webhook.url}
    </Text>
    <Flex justify="center" gap="xs" css={{ flex: 1 }}>
      <Tooltip openDelay={10} label="Delete">
        <ActionIcon color="red" variant="filled" on:click={deleteWebhook}>
          <Trash size={20} />
        </ActionIcon>
      </Tooltip>
    </Flex>
  </Flex>
</Box>
