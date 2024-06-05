<script lang="ts">
  import { HOME_SCREEN_ITEMS } from '$lib';
  import Card from '$lib/components/homepage/Card.svelte';
  import { Button, Flex, Grid, createStyles } from '@svelteuidev/core';

  const useStyles = createStyles(() => {
    return {
      root: {},
      mainText: {
        textAlign: 'center',
        fontSize: 100,
        padding: 20,
        backgroundImage: 'linear-gradient(to right, #ff6600, #ff66cc)',
        backgroundClip: 'text',
        color: 'transparent'
      },
      card: {
        padding: 50,
        height: '100%'
      },
      groupCard: {
        marginTop: 5,
        marginBottom: 15
      }
    };
  });

  $: ({ classes } = useStyles());
</script>

<Flex justify="center" direction="column" align="center" style="height:100%">
  <Grid>
    <Grid.Col span={12}>
      <div class={classes.mainText}>Welcome to Synthra</div>
    </Grid.Col>
    {#each HOME_SCREEN_ITEMS as item}
      <Grid.Col span={4} style="margin-bottom:2rem">
        <Card
          classes={classes.card}
          groupCardClasses={classes.groupCard}
          title={item.title}
          badgeTitle={item.badgeTitle}
          badgeColor={item.badgeColor}
          badgeVariant={item.badgeVariant}
          description={item.description}
        />
      </Grid.Col>
    {/each}
    <Grid.Col span={12} align="center">
      <a href="/auth/register">
        <Button variant="light" radius="md" style="width:25%">Register Now!</Button>
      </a>
    </Grid.Col>
  </Grid>
</Flex>
