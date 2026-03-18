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

smoke-transparent-fast-live:
	uv run python -m image_creator.smoke \
		--mode generate \
		--profile transparent_bg_fast \
		--prompt "Create a simple blue square centered on a transparent background." \
		--output-name smoke-transparent-fast-proof \
		--out-dir outputs/transparent_proofs
	file outputs/transparent_proofs/smoke-transparent-fast-proof.png

smoke-cutout-live:
	uv run python -m image_creator.smoke \
		--mode generate \
		--profile cutout \
		--prompt "Create a clean isolated product cutout of a white ceramic mug on a transparent background. Full object visible, clean silhouette, no extra objects." \
		--output-name smoke-cutout-proof \
		--out-dir outputs/transparent_proofs
	file outputs/transparent_proofs/smoke-cutout-proof.png

smoke-remove-bg-live:
	uv run python -m image_creator.smoke \
		--mode generate \
		--profile draft \
		--prompt "Clean product shot of a single red sneaker on a soft light gray studio background, centered, full object visible, realistic lighting, no text, no watermark." \
		--output-name smoke-remove-bg-source \
		--out-dir outputs/remove_bg_source >/dev/null
	uv run python -m image_creator.smoke \
		--mode remove_bg \
		--input-path outputs/remove_bg_source/smoke-remove-bg-source.jpg \
		--output-name smoke-remove-bg-proof \
		--out-dir outputs/remove_bg_result
	file outputs/remove_bg_result/smoke-remove-bg-proof.png

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
