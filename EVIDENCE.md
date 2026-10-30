# Capstone evidence guide

The referenced assignment preview contains only Tasks 1–3. Obtain the full 33-task rubric before matching later evidence to task numbers.

## Verified locally

- `python -m pytest -q --basetemp ../../work/pytest`: 3 passed on 30 October 2026.
- API routes and token checks are covered by `tests/test_accounts.py`.

## Tasks visible in the assignment preview

1. After publishing this project to a **public** GitHub repository, replace `OWNER` in `README.md` and confirm a successful Actions run. Submit the public README URL. The badge currently has a placeholder, so it is not evidence yet.
2. Submit the public URL of `user-story.md` after publishing.
3. Create the requested stories as real GitHub Issues and add them to the course Kanban board's **New Issues** column. Capture the actual board with all story cards visible. Save the image as `planning-userstories-done.png` or `.jpeg`. No board screenshot has been created here.

## Kanban story candidates

Use the `user-story.md` template for each issue, then set acceptance criteria to match your course labs:

- As a user, I need to create an account so that customer data is recorded.
- As a user, I need to list and retrieve accounts so that I can find customer information.
- As a user, I need to update an account so that customer details stay current.
- As a user, I need to delete an account so that obsolete records are removed.
- As an operator, I need health checks so that deployment failures are detected.
- As a maintainer, I need automated tests and builds so that changes are checked before release.
- As an operator, I need a container and Kubernetes deployment so that the service can run in a cluster.
- As a maintainer, I need a Tekton pipeline so that test and image build steps are repeatable.

## Evidence still requiring a real environment

- Public repository URLs, successful GitHub Actions run, and updated badge.
- Kanban board screenshots and sprint movement screenshots.
- Docker build output: local Docker build was blocked by access to Docker's build state.
- Kubernetes deployment output: no cluster connection is configured here.
- Tekton run output: no Tekton cluster is connected here.

Do not submit rendered examples or simulated terminal output as execution evidence. Run the commands in the target environment and capture the actual output.
