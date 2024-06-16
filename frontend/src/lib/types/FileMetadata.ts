export class FileMetadata {
  id: string;
  author: string;
  name: string;
  size: number;
  encrypted: string;
  shared: string;
  shared_people: FileShare[];
  path: string;
  timestamp: Date;
  expiration: Date;

  constructor(
    id: string,
    author: string,
    name: string,
    size: number,
    encrypted: string,
    shared: string,
    shared_people: FileShare[],
    timestamp: Date,
    expiration: Date,
    path: string
  ) {
    this.id = id;
    this.author = author;
    this.name = name;
    this.size = size;
    this.encrypted = encrypted;
    this.shared = shared;
    this.shared_people = shared_people;
    this.timestamp = timestamp;
    this.expiration = expiration;
    this.path = path;
  }
}

export class FileShare {
  id: string;
  username: string;

  constructor(id: string, username: string) {
    this.id = id;
    this.username = username;
  }
}
