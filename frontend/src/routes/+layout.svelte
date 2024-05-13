<script lang="ts">
  import { Header } from '$lib';
  import { AppShell, SvelteUIProvider, colorScheme, type ColorScheme } from '@svelteuidev/core';
  import { onMount } from 'svelte';

  function toggleTheme() {
    const newTheme = $colorScheme === 'light' ? 'dark' : 'light';
    colorScheme.update(() => newTheme);
    localStorage.setItem('theme', newTheme);
  }

  onMount(() => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
      colorScheme.update(() => savedTheme as ColorScheme);
    }
  });
</script>

<SvelteUIProvider withGlobalStyles themeObserver={$colorScheme}>
  <AppShell>
    <Header slot="header" {toggleTheme} currentTheme={$colorScheme}></Header>
    <slot>This is the main content</slot>
  </AppShell>
</SvelteUIProvider>
