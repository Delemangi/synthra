<script lang="ts">
  import { Button, Text, TextInput } from '@svelteuidev/core';
  import { isAxiosError } from 'axios';
  import { onMount } from 'svelte';
  import { register } from '../../../server/auth';
  import { isFieldSuitable } from '../../../utils/functions';

  let username = '';
  let password = '';
  let repeatPassword = '';

  const handleSubmit = async () => {
    if (password !== repeatPassword) {
      alert('Passwords do not match.');
      return;
    }

    try {
      await register(username, password);

      window.location.href = '/auth/login';
    } catch (error) {
      if (!isAxiosError(error)) {
        alert('An unknown error occurred.');
        return;
      }

      if (error.response?.status === 406) {
        alert('Username is already taken.');
        return;
      }

      alert('An error occurred while registering.');
    }
  };

  onMount(() => {
    let accessToken = localStorage.getItem('accessToken');

    if (accessToken) {
      window.location.href = '/';
    }
  });
</script>

<div
  style="width: 300px; margin: auto; top: 50%; transform: translate(0, 30vh); border: 1px solid gray; padding: 10px; border-radius: 5px"
>
  <TextInput label="Username (between 5 and 24 characters)" bind:value={username} />
  <TextInput label="Password (between 5 and 24 characters)" bind:value={password} type="password" />
  <TextInput label="Repeat Password" bind:value={repeatPassword} type="password" />
  <br />
  <div style="display: flex; justify-content: center;">
    <Button
      on:click={handleSubmit}
      disabled={!isFieldSuitable(username) || !isFieldSuitable(password)}
    >
      Register
    </Button>
  </div>
  <br />
  <Text align="center">
    Already have an account? <a href="/auth/register">Login!</a>
  </Text>
</div>
