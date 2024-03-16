<script lang="ts">
  import { createStyles, type DefaultTheme, ActionIcon, Box, Flex, Text, Tooltip, Anchor } from '@svelteuidev/core';
  import { File } from '../../types/File';
  import { Download, EyeOpen, Trash, ExternalLink } from 'radix-icons-svelte';

  export let file: File = new File('test', 'test', 1, 'test', new Date(2021, 1, 1), new Date(2021, 1, 1),'test');

  const useStyles = createStyles((theme : DefaultTheme) => {
        return {
          root: {
            [`${theme.dark} &`]: {
              bc: theme.fn.themeColor('dark', 5),
              color: 'white'
            },
            backgroundColor: '$gray50',
            textAlign: 'center',
            padding: '$10',
            borderRadius: '$md',
            '&:hover': {
                backgroundColor: '$gray100',
            },
          }
        }}
    );

    $: ({ classes, getStyles } = useStyles());

</script>

<Box
    class={getStyles()}
>
    <Flex align="center" justify="space-evenly" style="height: 100%;">
        <Text size="sm" css={{ flex: 1 }}>
            {file.name}
        </Text>
        <Text size="sm" css={{ flex: 1 }}>
            {file.encrypted}
        </Text>
        <Text size="sm" css={{ flex: 1 }}>
            {file.size}
        </Text>
        <Text size="sm" css={{ flex: 1 }}>
            {file.timestamp}
        </Text>
        <Text size="sm" css={{ flex: 1 }}>
          {file.expiration}
        </Text>
        <Flex justify="left" gap="xs" css={{ flex: 1 }}>
            <Tooltip openDelay={10} label="Preview">
              <Anchor href="/">
                <ActionIcon variant="filled"
                  color="blue">
                  <EyeOpen size={20} />
                </ActionIcon>
              </Anchor>
            </Tooltip>
            <Tooltip openDelay={10} label="Share">
              <Anchor href="/">
                <ActionIcon variant="filled"
                  color="cyan">
                  <ExternalLink size={20} />
                </ActionIcon>
              </Anchor>
            </Tooltip>
            <Tooltip openDelay={10} label="Download">
              <Anchor href="/">
                <ActionIcon variant="filled">
                  <Download size={20}/>
                </ActionIcon>
              </Anchor>
            </Tooltip>
            <Tooltip openDelay={10} label="Delete">
              <Anchor href="/">
                <ActionIcon
                  color="red"
                  variant="filled">
                  <Trash
                    size={20} />
                </ActionIcon>
              </Anchor>
            </Tooltip>
      </Flex>
    </Flex>
</Box>
