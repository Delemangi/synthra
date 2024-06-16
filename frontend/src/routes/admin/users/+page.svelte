<script lang="ts">
  import TitleUserRow from '$lib/components/admin/TitleUserRow.svelte';
  import UserRow from '$lib/components/admin/UserRow.svelte';
  import type { RoleMetadata } from '$lib/types/RoleMetadata';
  import type { UserMetadata } from '$lib/types/UserMetadata';
  import { Title } from '@svelteuidev/core';
  import { onMount } from 'svelte';
  import { getRoles, getUsers } from '../../../server/auth';

  let users: UserMetadata[] = [];
  let roles: RoleMetadata[] = [];

  onMount(async () => {
    const accessToken = localStorage.getItem('accessToken');

    if (!accessToken) {
      window.location.href = '/auth/login';
      return;
    }

    users = await getUsers(accessToken);
    roles = await getRoles(accessToken);
  });
</script>

<div
  style="display: flex; flex-direction: column; justify-content: center; align-items: center; margin-bottom: 2rem;"
>
  <Title order={1}>Users</Title>
</div>

<TitleUserRow />
{#each users as user}
  <UserRow {user} {roles} />
{/each}
