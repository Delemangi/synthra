<script lang="ts">
  import type { UserMetadata } from '$lib/types/UserMetadata';
  import { Anchor, Button, Flex, Text, Title } from '@svelteuidev/core';
  import { isAxiosError } from 'axios';
  import { LockClosed, LockOpen2 } from 'radix-icons-svelte';
  import { onMount } from 'svelte';
  import { getUserMetadata } from '../../../server/auth';
  import { getFilesForSpecifiedUser } from '../../../server/files';
  import { getPermanentToken } from '../../../server/sharex';
  import { generateShareXTemplate } from '../../../utils/functions';

  let user: UserMetadata | null = null;
  let numberOfFiles: number | null = null;
  let storageUsed: number | null = null;

  onMount(async () => {
    let accessToken = localStorage.getItem('accessToken');

    if (!accessToken) {
      window.location.href = '/auth/login';
      return;
    }

    try {
      const response = await getUserMetadata(accessToken);
      const files = await getFilesForSpecifiedUser(accessToken);
      numberOfFiles = files.length;
      storageUsed = files.reduce((acc, file) => acc + file.size, 0);

      user = response.data;
    } catch (error) {
      if (!isAxiosError(error)) {
        alert('An unknown error occurred.');
        return;
      }

      alert('An error occurred while fetching the user data.');
    }
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

<Flex justify="center" align="center" direction="column" gap="lg">
  <Title>Account</Title>
  <Text>Username: {user?.username}</Text>
  <Text>Role: {user?.role.toUpperCase()}</Text>

  <br />

  <Title>2FA</Title>
  {#if user?.is_2fa_enabled}
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
  {:else}
    <Anchor href="/user/2fa/?option=enable">
      <Flex justify="center" gap="md">
        <LockClosed />
        <Text>Enable 2FA</Text>
      </Flex>
    </Anchor>
  {/if}

  <br />

  <Title>ShareX</Title>
  <Button on:click={generateShareXConfig}>Generate ShareX Configuration</Button>

  <br />

  <Title>Quotas</Title>
  <Text>{numberOfFiles} / {user?.files_quota ?? 0} Files</Text>
  <Text
    >{storageUsed} / {user?.size_quota ?? 0} B ({((storageUsed ?? 0) / 1000 / 1000).toFixed(2)} MB)
  </Text>
</Flex>
