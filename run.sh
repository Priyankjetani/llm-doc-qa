#!/bin/bash

# ─────────────────────────────────────────
# llm-doc-qa — Docker runner script
# Usage:
#   ./run.sh          → build and start
#   ./run.sh stop     → stop containers
#   ./run.sh restart  → restart containers
#   ./run.sh logs     → view live logs
#   ./run.sh rebuild  → force rebuild image
# ─────────────────────────────────────────

COMPOSE_FILE="docker/docker-compose.yml"
APP_NAME="llm-doc-qa"

case "$1" in

  stop)
    echo "🛑 Stopping $APP_NAME..."
    docker compose -f $COMPOSE_FILE down
    echo "✅ Stopped."
    ;;

  restart)
    echo "🔄 Restarting $APP_NAME..."
    docker compose -f $COMPOSE_FILE down
    docker compose -f $COMPOSE_FILE up -d
    echo "✅ Restarted. Visit http://127.0.0.1:8000/docs"
    ;;

  logs)
    echo "📋 Showing logs for $APP_NAME (Ctrl+C to exit)..."
    docker logs -f $APP_NAME
    ;;

  rebuild)
    echo "🔨 Rebuilding $APP_NAME image..."
    docker compose -f $COMPOSE_FILE down
    docker compose -f $COMPOSE_FILE up --build -d
    echo "✅ Rebuilt and running. Visit http://127.0.0.1:8000/docs"
    ;;

  *)
    echo "🚀 Building and starting $APP_NAME..."
    docker compose -f $COMPOSE_FILE up --build -d
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ App is running!"
        echo "👉 Visit: http://127.0.0.1:8000/docs"
        echo ""
        echo "Other commands:"
        echo "  ./run.sh stop     → stop the app"
        echo "  ./run.sh restart  → restart the app"
        echo "  ./run.sh logs     → view live logs"
        echo "  ./run.sh rebuild  → rebuild after code changes"
    else
      echo ""
      echo "❌ Something went wrong. Run './run.sh logs' to see what happened."
    fi
    ;;

esac