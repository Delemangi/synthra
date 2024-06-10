<script lang="ts">
  import { Button, TextInput } from '@svelteuidev/core';
  import { get2faToken } from '../../../server/auth';
  import { onMount } from 'svelte';
  import QR from '@svelte-put/qr/img/QR.svelte';

  let code: string | null = null;
  let username: string = '';
  let password: string = '';

  async function fetchCode() {
    try {
      let accessToken = localStorage.getItem('accessToken');

      if (!accessToken) {
        window.location.href = '/auth/login';
        return;
      }

      code = (await get2faToken(username, password)).data.code;
    } catch (error) {
      console.error('Failed to fetch 2FA token:', error);
    }
  }
  onMount(async () => {});
</script>

{#if code == null}
  <div
    style="width: 300px; margin: auto; top: 50%; transform: translate(0, 30vh); border: 1px solid gray; padding: 10px; border-radius: 5px"
  >
    <h1>Please log in again to get a new 2FA token</h1>
    <TextInput label="Username" bind:value={username} />
    <TextInput label="Password" bind:value={password} type="password" />
    <br />
    <div style="display: flex; justify-content: center;">
      <Button on:click={fetchCode} disabled={!username.length || !password.length}>Login</Button>
    </div>
    <br />
  </div>
{/if}

{#if code != null}
  <h1>2FA token {code}</h1>

  <QR
    data="otpauth://totp/synthra:{username}?secret={code}&issuer=synthra"
    anchorOuterFill="blue"
    moduleFill="green"
    anchorInnerFill="blue"
    backgroundFill="lightblue"
    width="168"
    height="168"
  />
{/if}
