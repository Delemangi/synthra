<!-- Header.svelte -->
<script>
    import { createStyles, Switch, Header, Flex, Title } from '@svelteuidev/core';
    export let toggleTheme = () => {};
    export let currentTheme = 'light';

    const useStyles = createStyles((theme) => {
        return {
          root: {
            height: 80,
          },
          flex: {
            [`${theme.dark} &`]: {
              bc: theme.fn.themeColor('dark', 5),
              color: 'white'
            },
            backgroundColor: theme.fn.themeColor('gray', 1),
            paddingLeft: 20,
            paddingRight: 20,
          },
          leftOptions: {
            padding: 30
          }
        }}
    );

    $: ({ classes, getStyles } = useStyles());
</script>


<Header class={getStyles()} slot="header" >
  <Flex class={classes.flex} justify="space-between" align="center" style="height: 100%;">

    <a class={classes.leftOptions}
        href="/">
          <Title order={1}>
            Synthra
          </Title>
    </a>
    <Flex justify="space-between">
      <a class={classes.leftOptions}
          href="/auth/login">
            <Title order={3}>
                Log In
            </Title>
      </a>

      <Switch
        color="gray"
        on:change={toggleTheme}
        label={currentTheme == 'dark' ? 'Dark' : 'Light'}
        checked={currentTheme == 'dark'} />
    </Flex>
  </Flex>
</Header>
