<script lang="ts">
  import { Header } from '$lib';
  import { AppShell, SvelteUIProvider, colorScheme } from '@svelteuidev/core';
  import { onMount } from 'svelte';
  import { validate } from '../server/auth';

  const toggleTheme = () => {
    const newTheme = $colorScheme === 'light' ? 'dark' : 'light';

    colorScheme.update(() => newTheme);
    localStorage.setItem('theme', newTheme);
  };

  const updateTheme = () => {
    const savedTheme = localStorage.getItem('theme');

    if (!savedTheme || (savedTheme !== 'light' && savedTheme !== 'dark')) {
      return;
    }

    colorScheme.update(() => savedTheme);
  };

  const updateToken = async () => {
    console.log('1');

    const accessToken = localStorage.getItem('accessToken');

    if (!accessToken) {
      localStorage.setItem('accessToken', '');
      localStorage.setItem('username', '');
      return;
    }

    console.log('2');

    const { data } = await validate(accessToken);

    console.log(data);

    if (data.message === 'valid') {
      return;
    }

    console.log('3');

    localStorage.removeItem('accessToken');
    localStorage.removeItem('username');
  };

  onMount(() => {
    updateTheme();
    updateToken();
  });
</script>

<SvelteUIProvider withGlobalStyles themeObserver={$colorScheme}>
  <AppShell>
    <Header slot="header" {toggleTheme} currentTheme={$colorScheme}></Header>
    <slot></slot>
  </AppShell>
</SvelteUIProvider>
