<script lang="ts">
  import { Button, Text, TextInput } from '@svelteuidev/core';
  import { isAxiosError } from 'axios';
  import { login } from '../../../server/auth';

  let username = '';
  let password = '';

  const handleSubmit = async () => {
    let response;

    try {
      response = await login(username, password);

      localStorage.setItem('accessToken', response.data.access_token);
      localStorage.setItem('username', username);
      window.location.href = '/user/home';
    } catch (error) {
      if (!isAxiosError(error)) {
        alert('An unknown error occurred.');
        return;
      }

      if (error.response?.status === 401) {
        alert('Invalid username or password.');
        return;
      }

      alert('An error occurred while logging in.');
    }
  };
</script>

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
