# Capstone evidence guide

The complete 33-question rubric was supplied on 30 October 2026. Only submit output from an actual run or screenshot of the actual board.

## Verified locally

- `python -m pytest -q --basetemp ../../work/pytest3`: 4 passed on 30 October 2026.
- `python -m flake8 service tests`: passed on 30 October 2026.
- API routes and token checks are covered by `tests/test_accounts.py`.

## Public URL tasks

1. Replace `OWNER` in `README.md`, publish publicly, confirm a successful Actions run, and submit the README URL.
2. Submit the public URL of `user-story.md`.
7. Submit the public URL of `setup.cfg`.
21. Submit the public URL of `.github/workflows/ci-build.yaml`.
22. Submit the public URL of `service/__init__.py`.
29. Submit the public URL of `Dockerfile`.

## Text output tasks

13–17. Capture genuine `curl` commands and responses for create, list, read, update, and delete in `rest-create-done`, `rest-list-done`, `rest-read-done`, `rest-update-done`, and `rest-delete-done`. Local loopback requests were blocked in this runtime; use the OpenShift terminal or the actual deployed route.
19. Save all steps of a successful GitHub Actions run as `ci-workflow-done`.
23. Save passing nosetests output after Talisman and CORS as `security-headers-done`.
26. Save actual JSON from the running application on port 8080 as `kube-app-output`.
30. Save `docker images` or equivalent output with name, tag, image ID, created time, and size as `kube-images`.
31. Save `kubectl get deployment,pods,replicasets,services` output as `kube-deploy-accounts`.
32. Save complete Tekton PipelineRun logs as `pipelinerun.txt`.

## Screenshot tasks

Capture the actual Kanban board at each requested stage. These are distinct historical states, so take each screenshot before moving cards onward:

| Task | File name | Required board state |
| --- | --- | --- |
| 3 | `planning-userstories-done.png` | All stories in New Issues |
| 4 | `planning-productbacklog-done.png` | Stories in Ice Box |
| 5 | `planning-labels-done.png` | Stories in Product Backlog with Technical Debt or Enhancement labels |
| 6 | `planning-kanban-done.png` | Sprint Backlog with estimates and Sprint 1 |
| 8–12 | `rest-techdebt-done.png`, `read-accounts.png`, `list-accounts.png`, `update-accounts.png`, `delete-accounts.png` | Named stories in Done |
| 18 | `sprint2-plan.png` | Two Sprint 2 stories in Sprint Backlog |
| 20 | `ci-kanban-done.png` | CI story in Done |
| 24 | `security-kanban-done.png` | Security story in Done |
| 25 | `sprint3-plan.png` | Three Sprint 3 stories in Sprint Backlog |
| 27–28 | `kube-docker-done.png`, `kube-kubernetes-done.png` | Container and deployment stories in Done |
| 33 | `cd-pipeline-done.png` | CD pipeline story in Done |

## Kanban story candidates

Use the `user-story.md` template for each issue. The rubric names these stories exactly: “Setting up the development environment”; “Read an account from the service”; “List all accounts in the service”; “Update an account in the service”; “Delete an account from the service”; “Need the ability to automate continuous integration checks”; “Need to add security headers and CORS policies”; “Containerize your microservice using Docker”; “Deploy your Docker image to Kubernetes”; and “Create a CD pipeline to automate deployment to Kubernetes.” Add a create-account story to cover the CREATE function. Set estimates and sprint assignments on the real board.

## Evidence still requiring a real environment

- Public repository URLs, successful GitHub Actions run, and updated badge. GitHub web sign-in is currently required to create a new public repository.
- Kanban board screenshots and sprint movement screenshots.
- Docker build output: local Docker build was blocked by access to Docker's build state.
- Kubernetes deployment output: no cluster connection is configured here.
- Tekton run output: no Tekton cluster is connected here.

Do not submit rendered examples or simulated terminal output as execution evidence. Run the commands in the target environment and capture the actual output.
