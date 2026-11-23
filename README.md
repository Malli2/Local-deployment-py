# Local Deployment Py

A lightweight Python HTTP service that demonstrates building, testing, publishing,
and deploying a containerized application to a local Kubernetes cluster.

The application has no third-party Python dependencies and exposes health, status,
and root JSON endpoints.

## Features

- Standard-library Python web server
- Docker image built with Python 3.12
- Kubernetes Deployment and ClusterIP Service manifests
- Automated tests
- GitHub Actions CI/CD for a self-hosted Linux runner
- Automatic port forwarding to `localhost:30080`
- Container runs as a non-root user

## API endpoints

| Endpoint | Description |
| --- | --- |
| `GET /` | Application information and available endpoints |
| `GET /health` | Health check used by Kubernetes probes |
| `GET /api/v1/status` | Runtime name, version, environment, and platform |

Example:

```bash
curl http://localhost:30080/
curl http://localhost:30080/health
curl http://localhost:30080/api/v1/status
```

## Run locally

Python 3 is the only local requirement.

```bash
python3 app/app.py
```

The service listens on `0.0.0.0:8080` by default. Configure it with environment
variables:

```bash
PORT=8081 \
APP_NAME="My Local App" \
APP_VERSION="1.0.0" \
APP_ENV="local" \
python3 app/app.py
```

## Run with Docker

Build the image:

```bash
docker build -t local-deployment-py:latest .
```

Run the container:

```bash
docker run --rm -p 8080:8080 local-deployment-py:latest
```

Open <http://localhost:8080>.

## Deploy to Kubernetes

The Kubernetes manifests deploy two replicas from GHCR.

Requirements:

- Docker Desktop with Kubernetes enabled, or another Kubernetes cluster
- `kubectl` configured for the cluster
- Access to `ghcr.io/malli2/local-deployment-py`

If the registry image is private, create the pull secret referenced by the
Deployment:

```bash
kubectl create secret docker-registry ghcr-secret \
  --docker-server=ghcr.io \
  --docker-username="<github-username>" \
  --docker-password="<github-token>"
```

Apply the manifests:

```bash
kubectl apply -f k8s/
kubectl rollout status deployment/mts-demo --timeout=180s
```

Expose the Service:

```bash
./scripts/start-port-forward.sh
```

Stop port forwarding with:

```bash
./scripts/stop-port-forward.sh
```

The application is available at <http://localhost:30080>.

To use a different local port:

```bash
PORT=30081 ./scripts/start-port-forward.sh
```

## Run the tests

```bash
python3 -m unittest discover -s tests -v
```

The tests start an ephemeral HTTP server and verify the root, health, and status
responses.

## CI/CD

The `.github/workflows/ci-cd.yml` workflow runs on a self-hosted Linux runner for
pushes to `main` and manual dispatches.

It:

1. Checks Docker, Kubernetes, Python, and the active cluster.
2. Runs the unit tests.
3. Builds SHA-tagged and `latest` Docker images.
4. Pushes both images to GHCR.
5. Applies the Kubernetes manifests.
6. Updates the Deployment image and waits for a successful rollout.
7. Starts port forwarding and verifies the HTTP endpoints.

The separate `.github/workflows/runner-test.yml` workflow checks that the
self-hosted runner can access Docker and Kubernetes.

## Configuration

| Variable | Default | Purpose |
| --- | --- | --- |
| `PORT` | `8080` | HTTP listen port |
| `APP_NAME` | `MTS Deployment Platform` | Application name returned by the API |
| `APP_VERSION` | `dev` | Application version |
| `APP_ENV` | `local` | Runtime environment; Kubernetes deployment uses `kubernetes` |

## Project structure

```text
.
├── app/
│   └── app.py
├── k8s/
│   ├── deployment.yaml
│   └── service.yaml
├── scripts/
│   ├── start-port-forward.sh
│   └── stop-port-forward.sh
├── tests/
│   └── test_app.py
├── Dockerfile
└── README.md
```

## License

This project is licensed under the [MIT License](LICENSE).
