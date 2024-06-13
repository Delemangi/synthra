<script lang="ts">
  import type { UserMetadata } from '$lib/types/UserMetadata';
  import { Anchor, Flex, Text } from '@svelteuidev/core';
  import { LockClosed, LockOpen2 } from 'radix-icons-svelte';
  import { onMount } from 'svelte';
  import { getUserMetadata } from '../../../server/auth';

  let username: string | null = null;
  let user: UserMetadata | null = null;

  onMount(async () => {
    let accessToken = localStorage.getItem('accessToken');
    username = localStorage.getItem('username');

    if (!accessToken) {
      window.location.href = '/auth/login';
      return;
    }

    let response = await getUserMetadata(accessToken);

    if (response.status != 200) {
      window.location.href = '/auth/login';
      return;
    }

    user = response.data;
  });
</script>

<Text size="lg" align="center">Hi, {username}!</Text>
<br />

<Flex justify="center" align="center" direction="column" gap="lg">
  {#if user?.is_2fa_enabled}
    <Anchor href="/user/2fa/?option=enable">
      <Flex justify="center" gap="md">
        <LockClosed />
        <Text>Enable 2FA</Text>
      </Flex>
    </Anchor>
  {:else}
    <Anchor href="/user/2fa?option=disable">
      <Flex justify="center" gap="md">
        <LockOpen2 />
        <Text>Disable 2FA</Text>
      </Flex>
    </Anchor>
    <Anchor href="/user/2fa?option=enable">
      <Flex justify="center" gap="md">
        <LockClosed />
        <Text>Update 2FA</Text>
      </Flex>
    </Anchor>
  {/if}
</Flex>
