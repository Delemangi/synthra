<script lang="ts">
  import type { RoleMetadata } from '$lib/types/RoleMetadata';
  import {
    ActionIcon,
    Box,
    Button,
    Flex,
    NumberInput,
    Overlay,
    Text,
    Title,
    Tooltip,
    createStyles,
    type theme
  } from '@svelteuidev/core';
  import { isAxiosError } from 'axios';
  import { Update } from 'radix-icons-svelte';
  import { editRole } from '../../../server/auth';

  export let role: RoleMetadata;
  let filesQuota: number = role.quota_files;
  let spaceQuota: number = role.quota_size;

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
        marginTop: '$3',
        marginBottom: '$3'
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

  const saveRole = async () => {
    const accessToken = localStorage.getItem('accessToken');

    if (!accessToken) {
      window.location.href = '/auth/login';
      return;
    }

    try {
      await editRole(accessToken, role.id, spaceQuota, filesQuota);
      location.reload();
    } catch (error) {
      if (!isAxiosError(error)) {
        alert('An unknown error occurred.');
        return;
      }

      if (error.response?.status === 403) {
        alert('You do not have permission to edit this role.');
        return;
      }

      alert('An error occurred while editing the role.');
    }
  };

  let overlayShown = false;

  $: ({ classes, getStyles } = useStyles());
</script>

<Box class={getStyles()}>
  <Flex align="center" justify="space-evenly" style="height: 100%;">
    <Text size="sm" css={{ flex: 1, textAlign: 'center' }}>
      {role.name.toUpperCase()}
    </Text>
    <Text size="sm" css={{ flex: 1, textAlign: 'center' }}>
      {role.quota_files}
    </Text>
    <Text size="sm" css={{ flex: 1, textAlign: 'center' }}>
      {role.quota_size}
    </Text>
    <Flex justify="center" gap="xs" css={{ flex: 1 }}>
      <Tooltip openDelay={10} label="Edit">
        <ActionIcon variant="filled" color="blue" on:click={() => (overlayShown = true)}>
          <Update size={20} />
        </ActionIcon>
      </Tooltip>
    </Flex>
  </Flex>
</Box>

{#if overlayShown}
  <Overlay opacity={1} color="#000" zIndex={5} center class={classes.flexOverlay}>
    <Box class={getStyles()}>
      <Flex direction="column" align="space-evenly" gap="l" justify="center">
        <Title order={3}>Edit Role</Title>
        <NumberInput
          bind:value={filesQuota}
          placeholder="Files..."
          label="Files Quota"
          invalid={filesQuota < 0}
          hideControls
          required
        />
        <NumberInput
          bind:value={spaceQuota}
          placeholder="Space..."
          label="Space Quota"
          invalid={spaceQuota < 0}
          hideControls
          required
        />
        <Flex gap="lg" justify="space-between">
          <Button variant="filled" on:click={saveRole}>Submit</Button>
          <Button variant="light" on:click={() => (overlayShown = false)}>Close</Button>
        </Flex>
      </Flex>
    </Box>
  </Overlay>
{/if}
