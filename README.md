# Docker layer caching on GitHub Actions — demo

Builds the Dockerfile with a plain run step (`docker buildx build`) using the **GHA cache backend**:

- `--cache-from type=gha` — restore layers from the GitHub Actions cache
- `--cache-to type=gha,mode=max` — cache all intermediate layers (not just the final image)

The standard alternative is [docker/build-push-action], which is just a wrapper
around the same `docker buildx build` command with these flags as inputs.

## How the layers are laid out

| Layer | Content | Changes when |
|-------|---------|--------------|
| 1 | `apt-get install curl` | almost never |
| 2 | `pip install -r requirements.txt` | requirements.txt changes |
| 3 | `COPY server.py` | source changes |

## Try it

1. **Run 1 (cold)** — Actions → "Docker build" → "Run workflow". Everything builds from scratch (~1–2 min).
2. **Run 2 (no changes)** — run again. Log shows `CACHED` for every layer (~30s).
3. **Run 3 (source-only change)** — edit `server.py`, push. Layers 1–2 stay `CACHED`, only layer 3 rebuilds.
4. **Run 4 (dep change)** — add a package to `requirements.txt`, push. Layers 1 and 2 rebuild, 3 rebuilds too.

Look for `CACHED` lines in the "Build image" step log. Cache entries live in
Actions → Management → Caches (~10 GB limit per repo, evicted after ~7 days unused).

[docker/build-push-action]: https://github.com/docker/build-push-action
