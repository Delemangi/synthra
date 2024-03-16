<!-- Header.svelte -->
<script>
    import { Switch, Header, Flex, Title } from '@svelteuidev/core';

    export let toggleTheme = () => {};
    export let currentTheme = 'light';
</script>


<Header slot="header" height="50px">
  <Flex justify="space-between" align="center" style="height: 100%;">

    <a
        href="/">
          <Title order={1}>
            Synthra
          </Title>
    </a>
    <Flex justify="space-between">
      <a
          href="/auth/login">
            <Title order={3}>
                Log In
            </Title>
      </a>

      <Switch
        on:change={toggleTheme}
        checked={currentTheme == 'dark'} />
    </Flex>
  </Flex>
</Header>
