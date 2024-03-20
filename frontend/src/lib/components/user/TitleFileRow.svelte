<script lang="ts">
  import {
    createStyles,
    type DefaultTheme,
    Box,
    Flex,
    Text,
  } from '@svelteuidev/core';

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
        borderRadius: '$md',
        '&:hover': {
          backgroundColor: '$gray50'
        }
      },
      textStyle: {
        flex: 1
      }
    };
  });

  $: ({ classes, getStyles } = useStyles());
</script>

<Box class={getStyles()}>
  <Flex align="center" justify="space-evenly" style="height: 100%;">
    <Text size="sm" class={classes.textStyle}>File name</Text>
    <Text size="sm" class={classes.textStyle}>Encrypted</Text>
    <Text size="sm" class={classes.textStyle}>Size (MB)</Text>
    <Text size="sm" class={classes.textStyle}>Upload date</Text>
    <Text size="sm" class={classes.textStyle}>Expiration date</Text>
    <Text size="sm" class={classes.textStyle}>Actions</Text>
  </Flex>
</Box>
