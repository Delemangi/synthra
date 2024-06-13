<script lang="ts">
  import { page } from '$app/stores';
  import QR from '@svelte-put/qr/img/QR.svelte';
  import { Button, Flex, Text, TextInput } from '@svelteuidev/core';
  import { onMount } from 'svelte';
  import { get2faToken, remove2faToken } from '../../../server/auth';

  let code: string | null = null;
  let username: string = '';
  let password: string = '';
  let option: string | null = 'enable';

  const fetchCode = async () => {
    try {
      let accessToken = localStorage.getItem('accessToken');

      if (!accessToken) {
        window.location.href = '/auth/login';
        return;
      }

      if (option == 'enable') {
        code = (await get2faToken(username, password)).data.code;
      } else if (option == 'disable') {
        await remove2faToken(username, password);
        window.location.href = '/user/account';
        return;
      }
    } catch (error) {
      console.error('Failed to update 2FA token:', error);
    }
  };

  onMount(async () => {
    option = $page.url.searchParams.get('option');
  });
</script>

{#if code == null}
  <div class="container">
    <TextInput label="Username" bind:value={username} />
    <TextInput label="Password" bind:value={password} type="password" />
    <br />
    <div class="button-container">
      <Button on:click={fetchCode} disabled={!username.length || !password.length}>Login</Button>
    </div>
    <br />
  </div>
  <br />
  <Text size="md" align="center">Please log in again to update the 2FA token.</Text>
{/if}

{#if code != null}
  <Text align="center">Here is the QR code for your new authenticator:</Text>
  <br />

  <Flex justify="center">
    <QR
      data="otpauth://totp/synthra:{username}?secret={code}&issuer=synthra"
      anchorOuterFill="blue"
      moduleFill="green"
      anchorInnerFill="blue"
      backgroundFill="lightblue"
      width="168"
      height="168"
    />
  </Flex>

  <br />
  <Text align="center">Or, if you'd rather have the token:</Text>
  <br />
  <Text size="lg" align="center">{code}</Text>

  <br />

  <Flex justify="center">
    <Button>
      <a href="/user/account">Back</a>
    </Button>
  </Flex>
{/if}

<style>
  .container {
    width: 300px;
    margin: auto;
    top: 50%;
    transform: translate(0, 30vh);
    border: 1px solid gray;
    padding: 10px;
    border-radius: 5px;
  }

  .button-container {
    display: flex;
    justify-content: center;
  }
</style>
