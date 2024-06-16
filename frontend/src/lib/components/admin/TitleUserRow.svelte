<script lang="ts">
  import { Box, Flex, Text, createStyles, type DefaultTheme } from '@svelteuidev/core';

  const useStyles = createStyles((theme: DefaultTheme) => {
    return {
      root: {
        [`${theme.dark} &`]: {
          bc: theme.fn.themeColor('dark', 5),
          color: 'white'
        },
        backgroundColor: '$gray20',
        textAlign: 'center',
        padding: '$10',
        borderRadius: '$md'
      },
      textStyle: {
        flex: 1,
        textAlign: 'center'
      }
    };
  });

  $: ({ classes, getStyles } = useStyles());
</script>

<Box class={getStyles()}>
  <Flex align="center" justify="space-evenly" style="height: 100%;">
    <Text size="md" weight="bold" transform="uppercase" class={classes.textStyle}>Name</Text>
    <Text size="md" weight="bold" transform="uppercase" class={classes.textStyle}>Role</Text>
    <Text size="md" weight="bold" transform="uppercase" class={classes.textStyle}>Actions</Text>
  </Flex>
</Box>
