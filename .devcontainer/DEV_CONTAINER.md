# Working in a Dev Container

## Setup

If you'd like to work on this project in a Dev Container, follow these steps:

1. Install the [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension
2. Build and start the project in a Dev Container (`Dev Containers: Rebuild Container`)
3. When prompted, install all recommended extensions for working with this project
4. Install the dependencies in the `FastAPI` project: `cd backend && poetry install`
5. Install the dependencies in the `SvelteKit` project: `cd frontend && npm i`
6. Select the Python environment created by `Poetry`. If it does not appear in the menu, choose the option to manually find it. The location to the Python executable is `backend/.venv/bin/python.exe`
7. (Optional) Reload the extensions from the Python linters: `Ruff` and `MyPy`

You now have a working Dev Container. Within it is running a PostgreSQL database at all times, whose files are located in `.devcontainer/pg_data`, as well as all tooling (linters and such) which is required (or recommended) to work on this project.

## Caveats

Working in a Dev Container may simplify your setup, as it comes equipped with everything you probably need. However, the downsides of it are higher resource requirements from your computer, and you are also not able to access SSH and GPG keys from inside the Dev Container (which means that you cannot create Git commits, but you can still create them outside in a normal terminal).

If you rebuild the Dev Container, then all extensions, as well as everything that does not live inside of a volume, will be lost.

## Troubleshooting

If you get permission related errors when working with the file system, you will need to `chown` the files or directories to the user `vscode`.
