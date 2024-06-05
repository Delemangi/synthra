export class Webhook {
  id: string;
  url: string;
  platform: string;

  constructor(id: string, url: string, platform: string) {
    this.id = id;
    this.url = url;
    this.platform = platform;
  }
}
