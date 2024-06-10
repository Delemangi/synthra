<script lang="ts">
  import { Button, Text, TextInput } from '@svelteuidev/core';
  import { isAxiosError } from 'axios';
  import { login } from '../../../server/auth';
  import { onMount } from 'svelte';

  let username: string = '';
  let password: string = '';
  let code2FA: string | null = null;
  let code2FAInput: boolean = false;

  const handleSubmit = async () => {
    let response;

    try {
      response = await login(username, password, code2FA);

      localStorage.setItem('accessToken', response.data.access_token);
      localStorage.setItem('username', username);
      window.location.href = '/user/home';
    } catch (error) {
      if (!isAxiosError(error)) {
        alert('An unknown error occurred.');
        return;
      }

      if (error.response?.status === 302) {
        if (code2FAInput) {
          alert('Invalid 2FA code. Try again.');
          return;
        }
        code2FAInput = true;
        return;
      }

      if (error.response?.status === 401) {
        alert('Invalid username or password.');
        return;
      }

      alert('An error occurred while logging in.');
    }
  };

  onMount(() => {
    let accessToken = localStorage.getItem('accessToken');

    if (accessToken) {
      window.location.href = '/';
    }
  });
</script>

{#if !code2FAInput}
  <div
    style="width: 300px; margin: auto; top: 50%; transform: translate(0, 30vh); border: 1px solid gray; padding: 10px; border-radius: 5px"
  >
    <TextInput label="Username" bind:value={username} />
    <TextInput label="Password" bind:value={password} type="password" />
    <br />
    <div style="display: flex; justify-content: center;">
      <Button on:click={handleSubmit} disabled={!username.length || !password.length}>Login</Button>
    </div>
    <br />
    <Text align="center">
      No account? <a href="/auth/register">Register!</a>
    </Text>
  </div>
{/if}

{#if code2FAInput}
  <h1>2FA authentication enabled</h1>
  <p>Please open your authentication app and enter the code.</p>
  <div
    style="width: 300px; margin: auto; top: 50%; transform: translate(0, 30vh); border: 1px solid gray; padding: 10px; border-radius: 5px"
  >
    <TextInput label="Code" bind:value={code2FA} />
    <br />
    <div style="display: flex; justify-content: center;">
      <Button on:click={handleSubmit} disabled={!code2FA?.length}>Submit</Button>
    </div>
    <br />
  </div>
{/if}
