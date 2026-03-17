bootstrap:
	uv sync --dev

lint:
	uv run ruff check . --show-files

typecheck:
	uv run mypy src

test:
	uv run pytest

smoke:
	uv run python -c "from image_creator.server import build_server; build_server(); print('server-import-ok')"

smoke-live:
	uv run python -m image_creator.smoke

check: lint typecheck test smoke
