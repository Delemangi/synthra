<script>
  import { Header } from '$lib';
  import { AppShell, SvelteUIProvider, colorScheme } from '@svelteuidev/core';

  function toggleTheme() {
    colorScheme.update((v) => (v === 'light' ? 'dark' : 'light'));
  }
</script>

<SvelteUIProvider withGlobalStyles themeObserver={$colorScheme}>
  <AppShell>
    <Header slot="header" {toggleTheme} currentTheme={$colorScheme}></Header>
    <slot>This is the main content</slot>
  </AppShell>
</SvelteUIProvider>
