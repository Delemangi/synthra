<script lang="ts">
  import { Badge, Card, Group, Text, type BadgeVariant } from '@svelteuidev/core';

  export let badgeTitle: string = '';
  export let badgeColor: string = '';
  export let badgeVariant: BadgeVariant = 'light';
  export let title: string = '';
  export let description: string = '';
  export let classes: string = '';
  export let groupCardClasses: string = '';
</script>

<Card shadow="sm" padding="lg" class={classes}>
  <Group position="apart" class={groupCardClasses}>
    <Text weight={500}>{title}</Text>
    <Badge color={badgeColor} variant={badgeVariant}>
      {badgeTitle}
    </Badge>
  </Group>

  <Text size="sm">
    {description}
  </Text>
</Card>
