# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/engine/reference/builder/

ARG PYTHON_VERSION=3.11.4
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt


# Copy the source code into the container.
COPY . .

# Ensure the start.sh script has execute permissions
RUN chmod +x /app/start.sh

# Set the Scrapyd bind address to 0.0.0.0 via environment variable
ENV SCRAPYD_BIND_ADDRESS 0.0.0.0

# Copy Scrapyd configuration file
COPY scrapyd.conf /etc/scrapyd/

# Expose the port that the application listens on.
EXPOSE 6800


# run the shell script
CMD ["scrapyd"]
