<script lang="ts">
  import { createStyles, Badge, Button, Group, Grid, Text, Title, type DefaultTheme } from '@svelteuidev/core';
  import Card from '$lib/components/homepage/Card.svelte';
  import { HomeScreenInfo } from '$lib/types/HomeScreenInfo';

  const useStyles = createStyles((theme: DefaultTheme) => {
        return {
          root: {
          },
          mainText: {
            textAlign: 'center',
            fontSize: 50,
            padding: 20,
            backgroundImage: "linear-gradient(to right, #ff6600, #ff66cc)",
            backgroundClip: "text",
            color: "transparent"
          },
          card: {
            padding: 50,
            height: '100%'
          },
          groupCard: {
            marginTop: 5,
            marginBottom:15
          }
        }}
    );

    $: ({ classes, getStyles } = useStyles());

    let items : HomeScreenInfo[] = [
      new HomeScreenInfo (
        'Upload your files',
        'Upload your files to Synthra and access them from anywhere.',
        'Upload',
        'light',
        'pink',
      ),
      new HomeScreenInfo (
        'Share your files',
        'Share your files with friends and family by sending them a link to your file.',
        'Share',
        'light',
        'blue',
      ),
      new HomeScreenInfo (
        'Webhooks support',
        'Post your uploaded images to platforms that support webhooks!',
        'Webhooks',
        'light',
        'green',
      ),
      new HomeScreenInfo (
        'Save websites',
        'Save the websites using our extension',
        'Websites',
        'light',
        'gray',
      ),
      new HomeScreenInfo (
        'Browser preview',
        'Preview the files in the browser',
        'Preview',
        'light',
        'orange',
      ),
      new HomeScreenInfo (
        'ShareX support',
        'Full ShareX support!',
        'ShareX',
        'light',
        'cyan',
      ),
    ]

</script>

<Grid>
    <Grid.Col span={12}>
      <div
        class={classes.mainText}
        >
          Welcome to Synthra
    </div>
    </Grid.Col>
    {#each items as item}
      <Grid.Col span={4}>
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
    <Grid.Col span={12}>
      <Button
        variant="light"
        ripple
        radius="md"
        style="width:100%">
        Register Now!
      </Button>
    </Grid.Col>
</Grid>
