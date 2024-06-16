<script lang="ts">
  import { FileMetadata } from '$lib/types/FileMetadata';
  import {
    Box,
    Button,
    Checkbox,
    Flex,
    Overlay,
    Text,
    TextInput,
    Title,
    createStyles,
    type theme
  } from '@svelteuidev/core';
  import { onMount } from 'svelte';
  import { updateFileSecurityData } from '../../../server/files';
  import { isAxiosError } from 'axios';

  export let file = new FileMetadata(
    'test',
    'test',
    'test',
    1,
    'test',
    'test',
    [],
    new Date(2021, 1, 1),
    new Date(2021, 1, 1),
    'test'
  );

  let is_file_encrypted = false;
  let is_file_shared = false;
  let current_file_password = '';
  let new_file_password = '';
  let changed_password = false;
  let delete_password = false;

  export let visible = true;
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
        marginTop: '$3',
        marginBottom: '$3'
      },
      flexOverlay: {
        display: 'flex',
        height: '100%',
        justifyContent: 'center',
        alignItems: 'center',
        direction: 'column',
        backdropFilter: 'blur(5px)'
      }
    };
  });
  const sendData = async () => {
    const accessToken = localStorage.getItem('accessToken');

    if (!accessToken) {
      alert('You need to be logged in.');

      return;
    }

    is_file_encrypted = !delete_password && is_file_encrypted;

    try {
      await updateFileSecurityData(
        accessToken,
        file.id,
        is_file_encrypted,
        is_file_shared,
        current_file_password,
        new_file_password
      );
      window.location.reload();
    } catch (error) {
      if (!isAxiosError(error)) {
        alert('An unknown error occurred.');
        return;
      }

      if (error.response?.status === 404) {
        alert('That file does not exist.');
        return;
      }

      if (error.response?.status === 403) {
        alert('Invalid access credentials.');
        return;
      }

      if (error.response?.status === 400) {
        alert('Bad request');
        return;
      }

      alert('An error occurred while downloading the file.');
    }
  };

  onMount(() => {
    is_file_encrypted = Boolean(file.encrypted);
    is_file_shared = Boolean(file.shared);

    console.log(is_file_encrypted);
    console.log(is_file_shared);
  });

  $: ({ classes, getStyles } = useStyles());
</script>

<Overlay opacity={1} color="#000" zIndex={5} center class={classes.flexOverlay}>
  <Box class={getStyles()}>
    <Flex direction="column" align="space-evenly" gap="md" justify="center">
      <Title order={3}>File security</Title>

      <Flex justify="center" align="center" gap="md">
        <Checkbox bind:checked={is_file_shared}></Checkbox>
        <Text>Private?</Text>
      </Flex>
      {#if !file.encrypted}
        <Flex justify="center" align="center" gap="md">
          <Checkbox visible={!file.encrypted} bind:checked={is_file_encrypted}></Checkbox>
          <Text>Encrypt?</Text>
        </Flex>
      {/if}
      {#if file.encrypted}
        <Flex justify="center" align="center" gap="md">
          <Checkbox bind:checked={changed_password}></Checkbox>
          <Text>Change Password?</Text>
        </Flex>
      {/if}
      {#if file.encrypted && changed_password}
        <Flex justify="center" align="center" gap="md">
          <Checkbox bind:checked={delete_password} on:click={() => (new_file_password = '')}
          ></Checkbox>
          <Text>Delete Password</Text>
        </Flex>
      {/if}
      {#if changed_password || (!file.encrypted && is_file_encrypted)}
        <TextInput
          bind:value={new_file_password}
          disabled={delete_password}
          placeholder="Password..."
          type="password"
          label="Please enter the new password"
        />
      {/if}
      {#if file.encrypted}
        <TextInput
          bind:value={current_file_password}
          placeholder="Password..."
          type="password"
          label="Please enter the current password to save the changes"
        />
      {/if}
      <Flex justify="space-around" align="center">
        <Button
          variant="filled"
          on:click={sendData}
          disabled={(file.encrypted && !current_file_password) ||
            (changed_password && !new_file_password && !delete_password) ||
            (!file.encrypted && is_file_encrypted && !new_file_password)}
        >
          Submit
        </Button>
        <Button variant="light" on:click={() => (visible = false)}>Close</Button>
      </Flex>
    </Flex>
  </Box>
</Overlay>
