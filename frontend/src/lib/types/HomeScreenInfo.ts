import type { BadgeVariant } from '@svelteuidev/core';

export class HomeScreenInfo {
  title: string;
  description: string;
  badgeTitle: string;
  badgeVariant: BadgeVariant;
  badgeColor: string;

  constructor(
    title: string,
    description: string,
    badgeTitle: string,
    badgeVariant: BadgeVariant,
    badgeColor: string
  ) {
    this.title = title;
    this.description = description;
    this.badgeTitle = badgeTitle;
    this.badgeVariant = badgeVariant;
    this.badgeColor = badgeColor;
  }
}
