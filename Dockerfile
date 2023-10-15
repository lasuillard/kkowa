FROM python:3.11-slim-bookworm AS workspace

USER root:root

SHELL ["/bin/bash", "-c"]

# Core deps
RUN apt-get update && apt-get install --no-install-recommends -y \
    curl \
    gcc \
    git \
    gnupg2 \
    make \
    xvfb \
    # PyQt6
    libxkbcommon-x11-0 \
    libegl1 \
    libfontconfig \
    libglib2.0-0 \
    libdbus-1-3 \
    qtwayland5 \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL -o /usr/bin/grpc_health_probe "https://github.com/grpc-ecosystem/grpc-health-probe/releases/download/v0.4.21/grpc_health_probe-linux-$(dpkg --print-architecture)" \
    && chmod +x /usr/bin/grpc_health_probe

RUN pip install --no-cache-dir poetry

ARG WORKSPACE="/workspace"

WORKDIR "${WORKSPACE}"

# Dev tools
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Deps
COPY poetry.lock poetry.toml pyproject.toml ./
RUN poetry install --verbose --no-ansi --no-interaction --no-root --sync --with dev

VOLUME ["${WORKSPACE}/.venv"]

RUN git config --system --add safe.directory "${WORKSPACE}"

# Python control variables
ENV PYTHONUNBUFFERED="1"
ENV PYTHONPATH="${WORKSPACE}:${WORKSPACE}/_generated/grpc:${PYTHONPATH}"

HEALTHCHECK NONE
