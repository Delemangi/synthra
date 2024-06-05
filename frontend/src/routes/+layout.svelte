<script lang="ts">
  import { Header } from '$lib';
  import { AppShell, SvelteUIProvider, colorScheme } from '@svelteuidev/core';
  import { onMount } from 'svelte';

  const toggleTheme = () => {
    const newTheme = $colorScheme === 'light' ? 'dark' : 'light';

    colorScheme.update(() => newTheme);
    localStorage.setItem('theme', newTheme);
  };

  onMount(() => {
    const savedTheme = localStorage.getItem('theme');

    if (!savedTheme || (savedTheme !== 'light' && savedTheme !== 'dark')) {
      return;
    }

    colorScheme.update(() => savedTheme);
  });
</script>

<SvelteUIProvider withGlobalStyles themeObserver={$colorScheme}>
  <AppShell>
    <Header slot="header" {toggleTheme} currentTheme={$colorScheme}></Header>
    <slot></slot>
  </AppShell>
</SvelteUIProvider>
