<script lang="ts">
  import { page } from '$app/stores';
  import QR from '@svelte-put/qr/img/QR.svelte';
  import { Anchor, Button, Flex, Text, TextInput } from '@svelteuidev/core';
  import { isAxiosError } from 'axios';
  import { onMount } from 'svelte';
  import { get2FAToken, remove2FAToken } from '../../../server/auth';

  let code: string | null = null;
  let username: string | null = null;
  let password: string = '';
  let option: string | null = 'enable';

  const fetchCode = async () => {
    try {
      let accessToken = localStorage.getItem('accessToken');

      if (!accessToken || !username) {
        window.location.href = '/auth/login';
        return;
      }

      if (option == 'enable') {
        code = (await get2FAToken(username, password)).data.code;
      } else if (option == 'disable') {
        await remove2FAToken(username, password);
        window.location.href = '/user/account';
        return;
      }
    } catch (error) {
      if (!isAxiosError(error)) {
        alert('An unknown error occurred.');
        return;
      }

      if (error.response?.status === 401) {
        alert('Invalid password.');
        return;
      }

      alert('An error occurred while sharing the file.');
    }
  };

  onMount(async () => {
    option = $page.url.searchParams.get('option');
    username = localStorage.getItem('username');
  });
</script>

{#if code == null}
  <div class="container">
    <TextInput
      label="Password"
      bind:value={password}
      type="password"
      required
      placeholder="Password..."
    />
    <br />
    <div class="button-container">
      <Button on:click={fetchCode} disabled={!password.length}>Verify</Button>
    </div>
    <br />
  </div>
  <br />
  <Text size="md" align="center">Please enter your password again to update the 2FA token.</Text>
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
      <Anchor href="/user/account">Back</Anchor>
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
