# Build context is the REPO ROOT so the tufte-plots assets are available.
#   docker build -f example/Dockerfile -t <img> .
FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /work

# Deps first for layer caching.
COPY example/requirements.txt example/requirements.txt
RUN pip install --no-cache-dir -r example/requirements.txt

# Source: the example plus the tufte assets it imports.
COPY skills/tufte-plots/assets skills/tufte-plots/assets
COPY example example

RUN useradd -m runner && chown -R runner /work
USER runner

WORKDIR /work/example
ENV IN_CONTAINER=1
ENTRYPOINT ["./run.sh"]
