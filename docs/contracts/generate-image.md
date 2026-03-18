# `generate_image` contract

Canonical first tool for this repo.

## Intent

Give an agent one stable way to produce an image file that can be reused later in a workflow.

## Input

- `prompt: str` — required
- `profile: str` — optional curated profile such as `draft`, `quality`, `text_heavy`, `character_consistency`, `style_transfer`
- `provider: str` — optional; defaults to `openrouter`
- `model: str` — optional provider-specific override
- `out_dir: str` — optional output directory; defaults to `IMAGE_OUTPUT_DIR` or `./outputs`
- `aspect_ratio: str` — optional provider-supported ratio such as `1:1`, `16:9`, `9:16`
- `image_size: str` — optional provider-supported size such as `1K`, `2K`, `4K`
- `negative_prompt: str` — optional explicit constraints for things that must not appear
- `reference_images: list[{path, role}]` — optional role-tagged references; supported roles are `style`, `subject`, `object`, `character`, `layout`
- `output_name: str` — optional stable filename stem

## Success output

The MCP tool returns a structured object with this shape:

```json
{
  "path": "/abs/path/to/outputs/img-1234.png",
  "mime_type": "image/png",
  "provider": "gemini",
  "model": "gemini-3.1-flash-image-preview",
  "profile": "draft"
}
```

## Behavioral invariants

- return an absolute path
- write exactly one image file for the first version
- create the output directory if it does not exist
- do not leave a partial final file on failure
- if the requested `output_name` already exists, allocate a collision-safe sibling name instead of overwriting it
- explicit `model` overrides `profile` when both are provided
- invalid `provider` / `model` combinations fail early
- current Gemini-family reference limits are enforced: max 14 refs total, max 4 `character`, max 10 non-character
- keep provider-specific HTTP and response parsing inside adapter modules

## Provider mapping notes

### Gemini

- endpoint family: `models/{model}:generateContent`
- image bytes come from `candidates[0].content.parts[*].inlineData`
- current default model: `gemini-3.1-flash-image-preview`
- older stable option still available: `gemini-2.5-flash-image`

### OpenRouter

- endpoint: `/api/v1/chat/completions`
- send `modalities: ["image", "text"]` or provider-compatible equivalent
- image arrives in `choices[0].message.images[*].image_url.url` as a data URL
- current proven default model: `google/gemini-3.1-flash-image-preview`
- compatibility aliases like `google/gemini-2.5-flash-image-preview` are normalized to the proven stable model

## Curated profiles

- `draft` -> fast composition and iteration
- `quality` -> highest-fidelity final pass
- `text_heavy` -> typography and layout-critical assets
- `character_consistency` -> character-preserving generation with refs
- `style_transfer` -> restyling with composition preserved

### Future OpenAI adapter

- keep it as another provider module
- do not change the MCP tool shape just because transport differs

## Deliberate non-goals for v1

- no hidden prompt-optimizer sub-agent
- no multi-image batching
- no database
- no remote object store requirement
- no edit mode mixed into `generate_image`

## Source links

- Gemini image generation docs: <https://ai.google.dev/gemini-api/docs/image-generation>
- OpenRouter image generation docs: <https://openrouter.ai/docs/guides/overview/multimodal/image-generation>
- MCP build-server docs: <https://modelcontextprotocol.io/docs/develop/build-server>
