<script lang="ts">
  import type { RoleMetadata } from '$lib/types/RoleMetadata';
  import type { UserMetadata } from '$lib/types/UserMetadata';
  import {
    ActionIcon,
    Box,
    Button,
    Flex,
    NativeSelect,
    Overlay,
    Text,
    Title,
    Tooltip,
    createStyles,
    type theme
  } from '@svelteuidev/core';
  import { isAxiosError } from 'axios';
  import { StarFilled, Update } from 'radix-icons-svelte';
  import { clearSession } from '../../../auth/session';
  import { editUser } from '../../../server/auth';

  export let user: UserMetadata;
  export let roles: RoleMetadata[] = [];
  let role: string;

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

  const saveUser = async () => {
    const accessToken = localStorage.getItem('accessToken');

    if (!accessToken) {
      window.location.href = '/auth/login';
      return;
    }

    try {
      await editUser(accessToken, user.username, role);

      if (user.username === localStorage.getItem('username')) {
        window.location.href = '/user/account';
        return;
      }

      location.reload();
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

      if (error.response?.status === 403) {
        alert('You do not have permission to edit this user.');
        return;
      }

      alert('An error occurred while editing the user.');
    }
  };

  const openOverlay = () => {
    overlayShown = true;
    window.scrollTo(0, 0);
  };

  let overlayShown = false;

  $: ({ classes, getStyles } = useStyles());
</script>

<Box class={getStyles()}>
  <Flex align="center" justify="space-evenly" style="height: 100%;">
    <Text size="sm" css={{ flex: 1, textAlign: 'center' }}>
      {user.username}
    </Text>
    <Text size="sm" css={{ flex: 1, textAlign: 'center' }}>
      {user.role.toUpperCase()}
    </Text>
    <Flex justify="center" gap="xs" css={{ flex: 1 }}>
      <Tooltip openDelay={10} label="Edit">
        <ActionIcon variant="filled" color="blue" on:click={openOverlay}>
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
        <Title order={3}>Edit User</Title>
        <NativeSelect
          placeholder="Role..."
          label="Role"
          description="Pick a role"
          required
          data={roles.map((role) => {
            return { value: role.name, label: role.name.toUpperCase() };
          })}
          bind:value={role}
          icon={StarFilled}
        />
        <Flex gap="lg" justify="space-between">
          <Button variant="filled" on:click={saveUser} disabled={!role}>Submit</Button>

          <Button variant="light" on:click={() => (overlayShown = false)}>Close</Button>
        </Flex>
      </Flex>
    </Box>
  </Overlay>
{/if}
