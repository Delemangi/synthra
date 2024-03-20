<!-- Header.svelte -->
<script lang="ts">
  import { createStyles, Switch, Header, Flex, Title, type theme } from '@svelteuidev/core';
  export let toggleTheme = () => {};
  export let currentTheme = 'light';

  const useStyles = createStyles((theme: theme) => {
    return {
      root: {
        height: 80
      },
      flex: {
        [`${theme.dark} &`]: {
          bc: theme.fn.themeColor('dark', 5),
          color: 'white'
        },
        backgroundColor: theme.fn.themeColor('gray', 1),
        paddingLeft: 20,
        paddingRight: 20
      },
      leftOptions: {
        padding: 30
      },
      logo: {
        fontSize: 30,
        [`${theme.dark} &`]: {
          backgroundImage: 'linear-gradient(to right, pink, lightblue)'
        },
        backgroundImage: 'linear-gradient(to right, red, cyan)',
        backgroundClip: 'text',
        color: 'transparent'
      }
    };
  });

  $: ({ classes, getStyles } = useStyles());
</script>

<Header class={getStyles()} slot="header" height="50">
  <Flex class={classes.flex} justify="space-between" align="center" style="height: 100%;">
    <a class={classes.leftOptions} href="/">
      <div class={classes.logo}>Synthra</div>
    </a>
    <Flex justify="space-between">
      <a class={classes.leftOptions} href="/auth/login">
        <Title order={3}>Log In</Title>
      </a>

      <Switch
        color="gray"
        on:change={toggleTheme}
        label={currentTheme == 'dark' ? 'Dark' : 'Light'}
        checked={currentTheme == 'dark'}
      />
    </Flex>
  </Flex>
</Header>
