# Customer Accounts microservice

Project name: **Customer Accounts**

![Build and test](https://github.com/OWNER/customer-accounts/actions/workflows/ci.yml/badge.svg)

A Flask REST API backed by SQLite. It supports account creation, listing, retrieval, update, and deletion. Set `API_TOKEN` to require a bearer token for all account routes. `/health` remains public for probes.

## Run locally

```bash
pip install -r requirements-dev.txt
export DATABASE=./accounts.db API_TOKEN=change-me
flask --app service.app run
```

Use `Authorization: Bearer change-me` for `/accounts` requests.

```bash
pytest -q
ruff check service tests
docker build -t customer-accounts:local .
```

## Deployment

Replace `OWNER` in the badge and Kubernetes image with your GitHub owner. Build and push the image to your registry. Create `customer-accounts-secret` with key `api-token`, then apply `k8s/`. The SQLite PVC supports one replica; use a shared database before scaling horizontally. The Tekton pipeline requires an installed Hub resolver and registry credentials in its workspace service account.

## API

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/health` | Health check |
| GET | `/accounts` | List accounts |
| POST | `/accounts` | Create account |
| GET | `/accounts/{id}` | Get account |
| PUT | `/accounts/{id}` | Update fields |
| DELETE | `/accounts/{id}` | Delete account |
