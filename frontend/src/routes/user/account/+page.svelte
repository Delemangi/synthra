<script lang="ts">
  import type { UserMetadata } from '$lib/types/UserMetadata';
  import { Anchor, Button, Flex, Text } from '@svelteuidev/core';
  import { LockClosed, LockOpen2 } from 'radix-icons-svelte';
  import { onMount } from 'svelte';
  import { getUserMetadata } from '../../../server/auth';
  import { getPermanentToken } from '../../../server/sharex';
  import { generateShareXTemplate } from '../../../utils/functions';

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

  const generateShareXConfig = async () => {
    const accessToken = localStorage.getItem('accessToken');

    if (!accessToken) {
      window.location.href = '/auth/login';
      return;
    }

    const { access_token: shareXToken } = await getPermanentToken(accessToken);
    const template = generateShareXTemplate(shareXToken, window.location.origin);

    const stringifiedTemplate = JSON.stringify(template, null, 2);
    const blob = new Blob([stringifiedTemplate], { type: 'application/json' });
    const url = URL.createObjectURL(blob);

    const link = document.createElement('a');
    link.href = url;
    link.download = 'uploader.sxcu';

    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };
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

  <Button on:click={generateShareXConfig}>Generate ShareX Configuration</Button>
</Flex>
