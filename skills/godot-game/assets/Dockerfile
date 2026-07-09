# Headless Godot + matching export templates for CI game exports.
FROM debian:bookworm-slim

ARG GODOT_VERSION=4.3
ARG GODOT_RELEASE=stable
ARG GODOT_DIST=${GODOT_VERSION}-${GODOT_RELEASE}

RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates curl unzip \
    && rm -rf /var/lib/apt/lists/*

# Headless Godot binary (the standard Linux build runs with --headless).
RUN curl -fSL \
      "https://github.com/godotengine/godot/releases/download/${GODOT_DIST}/Godot_v${GODOT_DIST}_linux.x86_64.zip" \
      -o /tmp/godot.zip \
    && unzip /tmp/godot.zip -d /tmp \
    && mv /tmp/Godot_v${GODOT_DIST}_linux.x86_64 /usr/local/bin/godot \
    && chmod +x /usr/local/bin/godot \
    && rm /tmp/godot.zip

# Export templates must match the engine version exactly.
RUN curl -fSL \
      "https://github.com/godotengine/godot/releases/download/${GODOT_DIST}/Godot_v${GODOT_DIST}_export_templates.tpz" \
      -o /tmp/templates.tpz \
    && mkdir -p "/root/.local/share/godot/export_templates/${GODOT_VERSION}.${GODOT_RELEASE}" \
    && unzip /tmp/templates.tpz -d /tmp \
    && mv /tmp/templates/* "/root/.local/share/godot/export_templates/${GODOT_VERSION}.${GODOT_RELEASE}/" \
    && rm -rf /tmp/templates.tpz /tmp/templates

RUN godot --headless --version

WORKDIR /project
ENTRYPOINT ["godot", "--headless"]
