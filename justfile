# Qwen3-ASR backend — dev recipes, driven by uv. Recipe names parallel the
# other Super STT backends' justfiles so `just ci` means the same thing here.

# Set up / refresh the dev environment from uv.lock.
sync:
    uv sync

# Lint.
lint:
    uv run ruff check .

# Auto-format in place.
fmt:
    uv run ruff format .

# Check formatting without modifying (gating).
fmt-check:
    uv run ruff format --check .

# Static type check.
typecheck:
    uv run ty check

# Run the test suite. Extra args pass through, e.g. `just test -k cancel`.
test *args:
    uv run pytest {{ args }}

# Coverage: terminal summary + HTML report (htmlcov/) + JSON totals (coverage.json).
coverage *args:
    uv run pytest --cov=app --cov-report=term-missing --cov-report=html --cov-report=json {{ args }}

# Coverage as Cobertura XML (for CI artifacts / editor gutters).
coverage-xml:
    uv run pytest --cov=app --cov-report=term-missing --cov-report=xml

# Assemble a relocatable release bundle for one accelerator.
# Usage: just bundle [cpu|cuda13] [out-dir]
bundle accel="cpu" out="target":
    ./scripts/build_bundle.sh {{ accel }} {{ out }}

# Everything CI gates on (excludes the heavy bundle build).
ci: sync lint fmt-check typecheck test
