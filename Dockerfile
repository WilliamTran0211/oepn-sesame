# ------------- Alpine Linux Base --------------------------
# ────── Stage 1: Build all dependencies (Builder Stage) ──────
FROM python:3.13.3-alpine3.21 AS builder

# Install OS packages needed to compile some Python packages
RUN apk add --no-cache \
    build-base \
    libffi-dev \
    openssl-dev \
    musl-dev

WORKDIR /build

# Copy requirements and install Python dependencies into a specific prefix
COPY requirements.txt .
RUN pip install \
    --prefix=/install \
    --no-cache-dir \
    -r requirements.txt

# Copy your application code
COPY app ./app
# Compile Python code to .pyc files (optional, but can speed up app start)
RUN python -m compileall -q app

# ────── Stage 2: Runtime only (Final Stage) ──────
FROM python:3.13.3-alpine3.21

# Install only the minimal runtime OS libraries needed
# ffmpeg is included here as an example; only add what your app truly needs at runtime
RUN apk add --no-cache \
    libffi \
    openssl \
    ffmpeg

WORKDIR /app

# Copy the installed Python packages from the builder stage
COPY --from=builder /install /usr/local
# Copy the (compiled) application code from the builder stage
COPY --from=builder /build/app ./app

# Command to run the FastAPI app using Gunicorn
# Cloud Run and similar platforms will set the $PORT environment variable.
CMD exec gunicorn --bind :$PORT --workers 1 --worker-class uvicorn.workers.UvicornWorker -t 60 app.main:app
