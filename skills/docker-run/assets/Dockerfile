# Template image for a run.sh-driven workload. Adapt the base and deps.
FROM python:3.12-slim

# System deps (add as needed), then clean up to keep the image small.
RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /work

# Install Python deps first so the layer caches when only source changes.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run as non-root.
RUN useradd -m runner && chown -R runner /work
USER runner

# The container re-enters run.sh, which sees IN_CONTAINER=1 and runs the workload.
ENV IN_CONTAINER=1
ENTRYPOINT ["./run.sh"]
