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

smoke-transparent-live:
	uv run python -m image_creator.smoke \
		--mode generate \
		--profile transparent_bg \
		--prompt "Create a simple red circle centered on a transparent background." \
		--output-name smoke-transparent-proof \
		--out-dir outputs/transparent_proofs
	file outputs/transparent_proofs/smoke-transparent-proof.png

verify-model-catalog:
	uv run python -m image_creator.verify_model_catalog

smoke-edit-live:
	uv run python -m image_creator.smoke \
		--mode generate \
		--provider openrouter \
		--output-name smoke-edit-source \
		--out-dir outputs/smoke_edit_source >/dev/null
	uv run python -m image_creator.smoke \
		--mode edit \
		--provider openrouter \
		--input-path outputs/smoke_edit_source/smoke-edit-source.png \
		--prompt "Add black sunglasses to the banana. Keep the white background and simple flat illustration style." \
		--output-name smoke-edit-result \
		--out-dir outputs/smoke_edit_result

check: lint typecheck test smoke
