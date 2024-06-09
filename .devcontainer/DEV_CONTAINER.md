# Working in a Dev Container

## Setup

If you'd like to work on this project in a Dev Container, follow these steps:

1. Install the [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension
2. Build and start the project in a Dev Container (`Dev Containers: Rebuild Container`)
3. When prompted, install all recommended extensions for working with this project
4. (Optional) Reload the extensions from the Python linters: `Ruff` and `MyPy`

You now have a working Dev Container. Within it is running a PostgreSQL database at all times, whose files are located in `.devcontainer/pg_data`, as well as all tooling (linters and such) which is required (or recommended) to work on this project.

## Caveats

Working in a Dev Container may simplify your setup, as it comes equipped with everything you probably need. However, the downsides of it are higher resource requirements from your computer, and also you may not be able to access SSH and GPG keys from inside the Dev Container if you don't have valid OpenSSH and GPG versions installed (which means that you cannot create Git commits, but you can still create them outside in a normal terminal).

If you rebuild the Dev Container, then all extensions, as well as everything that does not live inside of a volume, will be lost.

## Troubleshooting

If you get permission related errors when working with the file system, you will need to `chown` the files or directories to the user `vscode`.

For any other problems, try reloading your window after building the container.
