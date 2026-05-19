# Dependency Upgrade Report — 2026-05-19

## Summary
- Total outdated: 4
- Safe to upgrade: 2
- Needs code changes: 2
- Hold back: 0
- Detected ecosystems: Python (pip + requirements.txt)

## Safe upgrades (will be applied in PR)

| Package | Ecosystem | From | To | Notable | Source |
|---------|-----------|------|-----|---------|--------|
| `python-dotenv` | pip | 1.2.1 | 1.2.2 | Patch bump. Breaking changes only affect `set_key`/`unset_key` and CLI `set`/`unset`, neither of which the caller uses (no direct import). | [release](https://github.com/theskumar/python-dotenv/releases/tag/v1.2.2) |
| `pyvesync` | pip | 3.3.3 | 3.4.2 | Bugfixes + new device models (Sprout, LV600S humidifier). No changes to `VeSync()`, `login()`, `update()`, `devices.air_purifiers`, `reset_filter()`, or `device_name`. | [releases](https://github.com/webdjoe/pyvesync/releases) |

## Needs code changes

### `fastapi` (0.128.0 → 0.136.1)
- **Required changes**:
  - Ensure runtime is Python ≥3.10 — Dockerfile uses `python:3.11-slim` (OK); local venv is 3.13 (OK).
  - **Strict Content-Type enforcement (0.132.0):** clients POSTing JSON must send `Content-Type: application/json`. `app.py` `reset_filters` has no body param so this likely does not apply to the current endpoint, but the README's `curl -X POST http://localhost:8000/reset-filters` example should be smoke-tested after upgrade. If issues surface, set `FastAPI(strict_content_type=False)` to preserve old behavior.
  - Transitive floor bumps: Starlette ≥0.46.0 (0.134.0), Pydantic ≥2.9.0 (0.135.2). Both auto-resolved by pip.
- **Deprecations**:
  - `ORJSONResponse` / `UJSONResponse` deprecated as of 0.131.0 (not used here).
- **Notable features**: Pydantic-Rust JSON serializer (~2× responses), native SSE (0.135.0), free-threaded 3.14t support.
- **Source**: [release notes](https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/release-notes.md)
- **Suggested follow-up**: a separate PR that bumps `fastapi>=0.136.0` after smoke-testing `/reset-filters` and `/health` with and without a `Content-Type` header.

### `uvicorn` (0.40.0 → 0.47.0)
- **Required changes**: None for the current usage. Agent reported **SAFE** because the caller invokes uvicorn purely via CLI (`uvicorn app:app --host 0.0.0.0 --port 8000`) — no programmatic API. Held to NEEDS_CHANGES per skill policy: any 0.x minor bump is semver-permitted to break, so it does not auto-merge.
- **Deprecations**: None observed in the range.
- **Notable features**: `--limit-max-requests-jitter` (0.41), `--reset-contextvars` (0.45), `ssl_context_factory` + eager ASGI import (0.47).
- **Source**: [releases](https://github.com/encode/uvicorn/releases)
- **Suggested follow-up**: bundle this with the fastapi bump above — they share the same release cadence and runtime.

## Hold back
*(none)*

## Methodology
- Agents dispatched: 4 (in 1 wave).
- Investigation failures (manual review needed): none.
- Skipped ecosystems (tooling missing): none.
- Test runner: project has no test suite. Upgrade verification is limited to `pip install -r requirements.txt` resolving cleanly + the FastAPI app importing.
- Note: `requirements.txt` uses `>=` floors only — there is no lockfile, so the running Docker image already pulls the floating latest at build time. Bumping the floor signals intent (and bounds future rollback) but does not change today's installed versions in a clean build.
