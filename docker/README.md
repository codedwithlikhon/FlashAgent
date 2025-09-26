# Docker setup for FlashAgent

This directory contains a fast, layered Docker build system designed to package
the Browser-Use/Playwright stack. Two Dockerfiles are provided:

- `Dockerfile` – A self-contained build that installs every dependency from
  scratch. Suitable when caching base images is not possible.
- `Dockerfile.fast` – Relies on the base images defined under `base-images/` to
  achieve < 30 second rebuilds once the base layers are prepared.

To build the base images run:

```bash
./docker/build-base-images.sh
```

Then build the final image:

```bash
docker build -f Dockerfile.fast -t browseruse .
```

Or fall back to the slower but self-contained Dockerfile:

```bash
docker build -t browseruse .
```
