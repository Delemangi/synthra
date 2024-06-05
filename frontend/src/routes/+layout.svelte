<script lang="ts">
  import { Header } from '$lib';
  import { AppShell, SvelteUIProvider, colorScheme } from '@svelteuidev/core';
  import { onMount } from 'svelte';
  import { clearSession } from '../auth/session';
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
    const accessToken = localStorage.getItem('accessToken');

    if (!accessToken) {
      clearSession();
      return;
    }

    const { data } = await validate(accessToken);

    if (data.message === 'valid') {
      return;
    }

    clearSession();
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
