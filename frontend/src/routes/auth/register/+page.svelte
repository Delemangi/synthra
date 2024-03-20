<script>
  import { TextInput, Button } from '@svelteuidev/core';

  let email = '';
  let password = '';
  let confirmPassword = '';

  async function handleSubmit() {
    try {
      if (password !== confirmPassword) {
        alert('Passwords do not match. Please confirm your password.');
        return;
      }

      const body = {
        username: email,
        password: password
      };
      const response = await fetch('http://localhost:8002/auth/register/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
      });

      if (response.ok) {
        window.location.href = '/auth/login';
      } else {
        alert('Register failed. Please check your credentials.');
      }
    } catch (error) {
      console.error('Error registering:', error);
      alert('An error occurred while registering. Please try again later.');
    }
  }
</script>

<div
  style="width: 300px; margin: auto; top: 50%; transform: translate(0, 30vh); border: 1px solid gray; padding:10px; border-radius:5px"
>
  <TextInput label="Email" bind:value={email} />
  <TextInput type="password" label="Password" bind:value={password} />
  <TextInput type="password" label="Confirm Password" bind:value={confirmPassword} />
  <br />
  <Button on:click={handleSubmit}>Register</Button>
</div>
