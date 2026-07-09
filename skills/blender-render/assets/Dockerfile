# Headless Blender (>=5) + ffmpeg for reproducible CI test renders (CPU).
# GPU rendering is done on the host via run_host.sh, not in this image.
FROM debian:bookworm-slim

ARG BLENDER_SERIES=5.0
ARG BLENDER_VERSION=5.0.0
ARG BLENDER_URL=https://download.blender.org/release/Blender${BLENDER_SERIES}/blender-${BLENDER_VERSION}-linux-x64.tar.xz

# Libraries Blender needs even in background mode, plus ffmpeg for encoding.
RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates curl xz-utils ffmpeg \
        libx11-6 libxi6 libxxf86vm1 libxfixes3 libxrender1 libxkbcommon0 \
        libgl1 libglu1-mesa libsm6 libxext6 libxrandr2 libfreetype6 \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fSL "$BLENDER_URL" -o /tmp/blender.tar.xz \
    && mkdir -p /opt/blender \
    && tar -xf /tmp/blender.tar.xz -C /opt/blender --strip-components=1 \
    && rm /tmp/blender.tar.xz \
    && ln -s /opt/blender/blender /usr/local/bin/blender

RUN blender --version

WORKDIR /work
ENTRYPOINT ["/bin/bash"]
