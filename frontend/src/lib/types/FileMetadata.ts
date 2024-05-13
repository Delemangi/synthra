export class FileMetadata {
  id: string;
  name: string;
  size: number;
  encrypted: string;
  path: string;
  timestamp: Date;
  expiration: Date;

  constructor(
    id: string,
    name: string,
    size: number,
    encrypted: string,
    timestamp: Date,
    expiration: Date,
    path: string
  ) {
    this.id = id;
    this.name = name;
    this.size = size;
    this.encrypted = encrypted;
    this.timestamp = timestamp;
    this.expiration = expiration;
    this.path = path;
  }
}
