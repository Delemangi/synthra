<script>
  import { TextInput, Button } from '@svelteuidev/core';
  import { Header } from '$lib';

  let email = '';
  let password = '';
  let accessToken = '';

  async function handleSubmit() {
    try {
      const formData = new FormData();
      formData.append('username', email);
      formData.append('password', password);

      const response = await fetch('http://localhost:8002/auth/login/', {
        method: 'POST',
        body: formData
      });

      if (response.ok) {
        const data = await response.json();
        accessToken = data.access_token;
        // Save the token to localStorage or sessionStorage
        localStorage.setItem('accessToken', accessToken);
        window.location.href = '/';
      } else {
        alert('Login failed. Please check your credentials.');
      }
    } catch (error) {
      console.error('Error logging in:', error);
      alert('An error occurred while logging in. Please try again later.');
    }
  }
</script>

<Header />

<div
  style="width: 300px; margin: auto; top: 50%; transform: translate(0, 30vh); border: 1px solid gray; padding:10px; border-radius:5px"
>
  <TextInput label="Email" bind:value={email} />
  <TextInput type="password" label="Password" bind:value={password} />
  <br />
  <Button on:click={handleSubmit}>Login</Button>
</div>
