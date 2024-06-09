#!/bin/bash

sudo mkdir /assets && sudo chown vscode /assets

cd /synthra/backend && poetry install --no-root
cd /synthra/frontend && npm i

poetry run pre-commit install
