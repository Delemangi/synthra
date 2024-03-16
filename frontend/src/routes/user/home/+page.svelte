<script>
  import { onMount } from "svelte";
  import { createStyles, Button, Box, Flex, Text, Overlay, Title } from "@svelteuidev/core";
  import FileRow from "$lib/components/user/FileRow.svelte";

  const useStyles = createStyles((theme) => {
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

    const response = await fetch('http://localhost:8002/files', {
      method: 'GET',
      headers: {
        authorization: `Bearer ${accessToken}`
      }
    });

    if (response.ok) {
      console.log('success'+ (await response.json()));
    }
    else {
      console.log('error');
    }
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
      <input type="file" id="myFile" name="filename">

      <Flex justify="space-around" align="center">
        <Button variant='filled' type="submit">Submit</Button>
        <Button variant='light' on:click={() => visible = false}>Close</Button>
      </Flex>
    </Flex>
  </Box>
</Overlay>
{/if}
