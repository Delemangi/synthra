<script lang="ts">
  import {
    createStyles,
    type theme,
    ActionIcon,
    Box,
    Flex,
    Text,
    Tooltip,
    Anchor
  } from '@svelteuidev/core';
  import { File } from '../../types/File';
  import { Download, EyeOpen, Trash, ExternalLink } from 'radix-icons-svelte';
  import { getCertainFileByPath } from '../../../axios/axios-request';

  export let file: File = new File(
    'test',
    'test',
    1,
    'test',
    new Date(2021, 1, 1),
    new Date(2021, 1, 1),
    'test'
  );

  const useStyles = createStyles((theme: theme) => {
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
          backgroundColor: '$gray100'
        }
      }
    };
  });

  async function getFile() : Promise<void>
  {
    try
    {
      let retrievedFile : void | globalThis.File = await getCertainFileByPath(localStorage.getItem('accessToken'), file.path);
      if(retrievedFile)
      {
        const url = URL.createObjectURL(retrievedFile);
        const a = document.createElement('a');
        a.href = url;
        a.download = file.name;
        a.click();
        URL.revokeObjectURL(url);
      }
    }
    catch(e)
    {
      console.log(e);
    }
  }

  $: ({ getStyles } = useStyles());
</script>

<Box class={getStyles()}>
  <Flex align="center" justify="space-evenly" style="height: 100%;">
    <Text size="sm" css={{ flex: 1 }}>
      {file.name}
    </Text>
    <Text size="sm" css={{ flex: 1 }}>
      {file.encrypted}
    </Text>
    <Text size="sm" css={{ flex: 1 }}>
      {Math.round(file.size / 1024)}
    </Text>
    <Text size="sm" css={{ flex: 1 }}>
      {file.timestamp}
    </Text>
    <Text size="sm" css={{ flex: 1 }}>
      {file.expiration}
    </Text>
    <Flex justify="left" gap="xs" css={{ flex: 1 }}>
      <Tooltip openDelay={10} label="Preview">
          <ActionIcon variant="filled" color="blue">
            <EyeOpen size={20} />
          </ActionIcon>
      </Tooltip>
      <Tooltip openDelay={10} label="Share">
        <ActionIcon variant="filled" color="cyan">
          <ExternalLink size={20} />
        </ActionIcon>
      </Tooltip>
      <Tooltip openDelay={10} label="Download">
        <ActionIcon variant="filled" on:click={getFile}>
          <Download size={20} />
        </ActionIcon>
      </Tooltip>
      <Tooltip openDelay={10} label="Delete">
        <ActionIcon color="red" variant="filled">
          <Trash size={20} />
        </ActionIcon>
      </Tooltip>
    </Flex>
  </Flex>
</Box>
