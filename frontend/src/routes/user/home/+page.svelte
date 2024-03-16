<script lang="ts">
  import { onMount } from "svelte";
  import { createStyles, Button, Box, Flex, Text, Overlay, Title, type DefaultTheme } from "@svelteuidev/core";
  import FileRow from "$lib/components/user/FileRow.svelte";
  import { getFilesForSpecifiedUser, sendFileForSpecifiedUser } from "../../../axios/axios-request";

  let files : FileList | null = null;

  function sendData() {
    if (files != null) {
      console.log(files);
      sendFileForSpecifiedUser(localStorage.getItem('accessToken'), files[0]);
    }
    else
    {
      console.log("No file selected");

    }
  }
  const useStyles = createStyles((theme : DefaultTheme) => {
      return {
        root: {
          [`${theme.dark} &`]: {
            bc: theme.fn.themeColor('dark', 5),
            color: 'white'
          },
          height: "100%",
          backgroundColor: theme.fn.themeColor('gray', 1),
          opacity: 1,
          padding: 20
        },
        flexOverlay: {
          display: "flex",
          height: "100%",
          justifyContent: "center",
          alignItems: "center",
          direction: "column",
          backdropFilter: "blur(5px)"
        },
      }}
  );

  $: ({ classes, getStyles } = useStyles());

  onMount(async function () {
    let accessToken = localStorage.getItem('accessToken');
    const response = await getFilesForSpecifiedUser(accessToken);
    console.log(response);
  });
  let visible = false;
</script>

<Button on:click={() => visible = !visible}>Upload file</Button>
<FileRow></FileRow>

{#if visible}
<Overlay opacity={0.9} color="#000" zIndex={5} center class={classes.flexOverlay}>
  <Box class={getStyles()}>
    <Flex direction="column" align="space-evenly" gap="md" justify="center">
      <Title order={3}>Upload your file</Title>

      <input type="file" id="myFile" name="filename" bind:files>

      <Flex justify="space-around" align="center">
        <Button variant='filled' on:click={sendData}>Submit</Button>
        <Button variant='light' on:click={() => visible = false}>Close</Button>
      </Flex>
    </Flex>
  </Box>
</Overlay>
{/if}
