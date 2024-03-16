export class File {
    id: string;
    name: string;
    size: number;
    isEncrypted: string;
    timestamp: Date;
    expiration: Date;

    constructor(id: string, name: string, size: number, type: string, timestamp: Date, expiration: Date) {
      this.id = id;
      this.name = name;
      this.size = size;
      this.isEncrypted = type;
      this.timestamp = timestamp;
      this.expiration = expiration;
    }
}
