#!/bin/bash

# ─────────────────────────────────────────
# llm-doc-qa — Docker + Kubernetes runner
# Usage:
#   ./run.sh               → build and start with Docker
#   ./run.sh stop          → stop Docker containers
#   ./run.sh restart       → restart Docker containers
#   ./run.sh logs          → view Docker live logs
#   ./run.sh rebuild       → force rebuild Docker image
#   ./run.sh k8s-deploy    → deploy to Kubernetes
#   ./run.sh k8s-open      → open app from Kubernetes
#   ./run.sh k8s-status    → check pods and services
#   ./run.sh k8s-logs      → view Kubernetes logs
#   ./run.sh k8s-stop      → remove Kubernetes deployment
# ─────────────────────────────────────────

# Add homebrew to PATH so minikube and kubectl work inside script
export PATH="/opt/homebrew/bin:$PATH"

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

  k8s-deploy)
    echo "☸️  Deploying to Kubernetes..."

    # Load your local Docker image into minikube
    echo "📦 Loading Docker image into minikube..."
    minikube image load llm-doc-qa:latest

    # Copy GCP key into minikube node
    echo "🔑 Copying GCP key into minikube..."
    minikube cp ./gcp-key.json /app/gcp-key.json

    # Apply all kubernetes files
    kubectl apply -f kubernetes/configmap.yaml
    kubectl apply -f kubernetes/deployment.yaml
    kubectl apply -f kubernetes/service.yaml

    echo ""
    echo "✅ Deployed to Kubernetes!"
    echo "⏳ Waiting for pods to start..."
    kubectl rollout status deployment/llm-doc-qa
    echo ""
    echo "👉 Run './run.sh k8s-open' to open in browser"
    ;;

  k8s-open)
    echo "🌐 Opening app from Kubernetes..."
    minikube service llm-doc-qa-service
    ;;

  k8s-status)
    echo "📊 Kubernetes status:"
    echo ""
    echo "--- PODS ---"
    kubectl get pods
    echo ""
    echo "--- SERVICES ---"
    kubectl get services
    echo ""
    echo "--- DEPLOYMENTS ---"
    kubectl get deployments
    ;;

  k8s-logs)
    echo "📋 Logs from Kubernetes pods..."
    kubectl logs -l app=llm-doc-qa --tail=50
    ;;

  k8s-stop)
    echo "🛑 Removing Kubernetes deployment..."
    kubectl delete -f kubernetes/service.yaml
    kubectl delete -f kubernetes/deployment.yaml
    kubectl delete -f kubernetes/configmap.yaml
    echo "✅ Kubernetes deployment removed."
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
      echo "  ./run.sh stop          → stop Docker app"
      echo "  ./run.sh restart       → restart Docker app"
      echo "  ./run.sh logs          → view Docker logs"
      echo "  ./run.sh rebuild       → rebuild Docker image"
      echo "  ./run.sh k8s-deploy    → deploy to Kubernetes"
      echo "  ./run.sh k8s-open      → open app from Kubernetes"
      echo "  ./run.sh k8s-status    → check pods and services"
      echo "  ./run.sh k8s-logs      → view Kubernetes logs"
      echo "  ./run.sh k8s-stop      → remove Kubernetes deployment"
    else
      echo ""
      echo "❌ Something went wrong. Run './run.sh logs' to see what happened."
    fi
    ;;

esac