# Docker layer caching on GitHub Actions

Minimal demo: a 3-layer Dockerfile built in CI with the **GHA cache backend**,
so unchanged layers are restored instead of rebuilt.

```yaml
- uses: docker/setup-buildx-action@v3
- uses: docker/build-push-action@v6
  with:
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

## Layers

| Layer | Content | Rebuilds when |
|-------|---------|---------------|
| 1 | `apt-get install curl` | Dockerfile changes |
| 2 | `pip install -r requirements.txt` | requirements.txt changes |
| 3 | `COPY server.py` | any source change |

Layer order matters: least-frequent changes first, most-frequent last.

## Verified results (ubuntu-latest)

| Run | Change | Build step | Layers |
|-----|--------|-----------|--------|
| 1 | — (cold) | ~27s | all built |
| 4 | source only | ~3s | apt + pip `CACHED`, only `COPY` rebuilt |

Cache entries: Actions → Management → Caches. Limits: 10 GB per repo,
~7 days idle eviction.

## Gotcha

`type=gha` only works through `build-push-action` (it wires the cache-service
token into buildkit). Passing `--cache-to type=gha` to `docker buildx build`
in a plain `run:` step silently does nothing — verified the hard way.
Use `build-push-action`.
