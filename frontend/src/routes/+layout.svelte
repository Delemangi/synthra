<script lang="ts">
  import { Header, COLOR_THEME_SCHEMA } from '$lib';
  import { AppShell, SvelteUIProvider, colorScheme } from '@svelteuidev/core';
  import { onMount } from 'svelte';

  const toggleTheme = () => {
    const newTheme = $colorScheme === 'light' ? 'dark' : 'light';

    colorScheme.update(() => newTheme);
    localStorage.setItem('theme', newTheme);
  };

  onMount(() => {
    const savedTheme = localStorage.getItem('theme');
    const { data, success } = COLOR_THEME_SCHEMA.safeParse(savedTheme);

    if (!success) {
      return;
    }

    colorScheme.update(() => data);
  });
</script>

<SvelteUIProvider withGlobalStyles themeObserver={$colorScheme}>
  <AppShell>
    <Header slot="header" {toggleTheme} currentTheme={$colorScheme}></Header>
    <slot></slot>
  </AppShell>
</SvelteUIProvider>
