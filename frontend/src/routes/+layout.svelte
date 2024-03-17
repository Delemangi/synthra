<script>
  import { colorScheme, SvelteUIProvider, AppShell, Button } from '@svelteuidev/core';
  import { Header } from '$lib';

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
