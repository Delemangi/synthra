<script lang="ts">
  import RoleRow from '$lib/components/admin/RoleRow.svelte';
  import TitleRoleRow from '$lib/components/admin/TitleRoleRow.svelte';
  import type { RoleMetadata } from '$lib/types/RoleMetadata';
  import { Title } from '@svelteuidev/core';
  import { onMount } from 'svelte';
  import { getRoles } from '../../../server/auth';

  let roles: RoleMetadata[] = [];

  onMount(async () => {
    const accessToken = localStorage.getItem('accessToken');

    if (!accessToken) {
      window.location.href = '/auth/login';
      return;
    }

    roles = await getRoles(accessToken);
  });
</script>

<div
  style="display: flex; flex-direction: column; justify-content: center; align-items: center; margin-bottom: 2rem;"
>
  <Title order={1}>Roles</Title>
</div>

<TitleRoleRow />
{#each roles as role}
  <RoleRow {role} />
{/each}
