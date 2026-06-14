#!/bin/bash
set -e

PORT=${2:-8000}

case "$1" in
    start)
        exec granian app.main.run:make_app --factory --interface asgi --host 0.0.0.0 --port "$PORT" --reload
        ;;
    *)
        exec "$@"
        ;;
esac
