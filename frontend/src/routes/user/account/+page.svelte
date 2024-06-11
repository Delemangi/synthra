<script lang="ts">
  import { Anchor, Text } from '@svelteuidev/core';
  import { onMount } from 'svelte';
  import { LockClosed, LockOpen2 } from 'radix-icons-svelte';
  import type { UserMetadata } from '$lib/types/UserMetadata';
  import { getUserMetadata } from '../../../server/auth';

  let username: string | null = '';
  let user: UserMetadata | null = null;

  onMount(async () => {
    let accessToken = localStorage.getItem('accessToken');

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

<Text>Hi, {username}</Text>

{#if user?.is_2fa_enabled}
  <Anchor href="/user/2fa/?option=enable">
    <LockClosed />
    <p>Enable 2FA</p>
  </Anchor>
{:else}
  <Anchor href="/user/2fa?option=disable">
    <LockOpen2 />
    <p>Disable 2FA</p>
  </Anchor>
  <Anchor href="/user/2fa?option=enable">
    <LockClosed />
    <p>Update 2FA</p>
  </Anchor>
{/if}
