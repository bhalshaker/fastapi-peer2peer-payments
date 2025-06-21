FROM python:3.12-slim

# Use root user explicitly
USER root

# Update and install dependencies
RUN apt-get update \
    && export DEBIAN_FRONTEND=noninteractive \
    && apt-get install -y --no-install-recommends \
    postgresql-client \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory (will be created by the volume mount)
WORKDIR /workspace


# Note: requirements.txt will be mounted via volume and installed in the postCreateCommand

# Set environment variables
ENV PYTHONPATH=/workspace
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# [Optional] Keep the container running
CMD ["sleep", "infinity"]