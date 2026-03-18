from __future__ import annotations

import json
from urllib.request import urlopen

from image_creator.image_profiles import OPENROUTER_CATALOG_MODELS


def main() -> None:
    with urlopen("https://openrouter.ai/api/v1/models", timeout=30) as response:  # noqa: S310
        payload = json.load(response)

    available_models = {entry["id"] for entry in payload.get("data", [])}
    missing_models = [model for model in OPENROUTER_CATALOG_MODELS if model not in available_models]

    if missing_models:
        raise SystemExit(
            "Missing curated OpenRouter image models: " + ", ".join(missing_models)
        )

    print("catalog-ok")
    for model in OPENROUTER_CATALOG_MODELS:
        print(model)


if __name__ == "__main__":
    main()
