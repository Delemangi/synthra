<script>
  import { TextInput, Button } from '@svelteuidev/core';
  import { Header } from '$lib';

  let email = '';
  let password = '';

  async function handleSubmit() {
    try {
      // Make API call to log in the user
      const formData = new URLSearchParams();
      formData.append('username', email);
      formData.append('password', password);

      const response = await fetch('http://localhost:8002/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: formData
      });

      if (response.ok) {
        // Redirect if login successful
        window.location.href = '/';
      } else {
        // Show alert if login failed
        alert('Login failed. Please check your credentials.');
      }
    } catch (error) {
      console.error('Error logging in:', error);
      alert('An error occurred while logging in. Please try again later.');
    }
  }
</script>

<Header/>
<div style="width: 300px; margin: auto; top: 50%; transform: translate(0, 30vh); border: 1px solid gray; padding:10px; border-radius:5px">
  <TextInput label='Email' bind:value={email} />
  <TextInput type='password' label='Password' bind:value={password} />
  <br/>
  <Button on:click={handleSubmit}>Login</Button>
</div>
