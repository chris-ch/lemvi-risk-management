#!/usr/bin/env bash

echo "executing entrypoint..."
/home/appuser/.local/bin/poetry install --no-root --no-interaction --directory=/workspaces/lemvi-rm > poetry-install.log 2>&1

exec "$@"
