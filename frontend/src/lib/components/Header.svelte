<script lang="ts">
  import { page } from '$app/stores';
  import {
    ActionIcon,
    Button,
    Flex,
    Header,
    Switch,
    Title,
    createStyles,
    type theme
  } from '@svelteuidev/core';
  import { onMount } from 'svelte';
  import { writable } from 'svelte/store';
  import { clearSession } from '../../auth/session';
  import { Person } from 'radix-icons-svelte';

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
      },
      selectedTab: {
        textDecoration: 'underline'
      }
    };
  });

  let accessToken: string | null = null;
  let username: string | null = null;

  export const selectedTab = writable('');

  const handleLogout = async () => {
    await clearSession(true);

    window.location.href = '/';
  };

  onMount(() => {
    accessToken = localStorage.getItem('accessToken');
    username = localStorage.getItem('username');
  });

  $: {
    const path = $page.url.pathname.split('/').at(-1) ?? '';
    selectedTab.set(path);
  }
  $: ({ classes, getStyles } = useStyles());
</script>

<Header class={getStyles()} slot="header" height="50">
  <Flex class={classes.flex} align="center" justify="space-between" style="height: 100%;">
    <Flex align="center">
      <a class={classes.leftOptions} href="/">
        <div class={classes.logo}>Synthra</div>
      </a>
      <Switch
        color="gray"
        on:change={toggleTheme}
        label={currentTheme == 'dark' ? 'Dark' : 'Light'}
        checked={currentTheme == 'dark'}
      />
    </Flex>

    <Flex align="center">
      {#if accessToken}
        <a
          class={classes.leftOptions + ($selectedTab === 'home' ? ` ${classes.selectedTab}` : '')}
          href="/user/home"
        >
          <Title order={3}>Files</Title>
        </a>

        <a
          class={classes.leftOptions +
            ($selectedTab === 'webhooks' ? ` ${classes.selectedTab}` : '')}
          href="/user/webhooks"
        >
          <Title order={3}>Webhooks</Title>
        </a>

        <Title order={3} style="padding: 15px">Hello, {username}!</Title>
      {/if}

      {#if accessToken}
        <Flex align="center">
          <Button variant="light">
            <a class={classes.leftOptions} href="/" on:click={handleLogout}>
              <Title order={3}>Logout</Title>
            </a>
          </Button>

          <ActionIcon
            variant={$selectedTab == 'account' ? 'filled' : 'light'}
            color="blue"
            on:click={() => (window.location.href = '/user/account')}
          >
            <Person size={20} />
          </ActionIcon>
        </Flex>
      {:else}
        <Button variant="light">
          <a class={classes.leftOptions} href="/auth/login">
            <Title order={3}>Login</Title>
          </a>
        </Button>
      {/if}
    </Flex>
  </Flex>
</Header>
