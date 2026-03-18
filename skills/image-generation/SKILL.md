---
name: image-generation
description: Use when the user wants to generate or edit images through the local `image_creator` MCP server — especially when the agent should pick the right image profile or model, use reference images, iterate drafts into final assets, or produce style-transfer / character-consistent edits saved to disk.
---

# Image Generation

Use this skill when image quality depends on choosing the right profile, composing a clean prompt, and using the local `image_creator` MCP server effectively.

This skill is not a rule pile. It is a compact knowledge layer for:
- choosing the right image profile,
- prompting efficiently,
- using reference images correctly,
- converging to a strong result through generate -> edit loops.

## Start here

Unless the user already specified an exact model or you already know the right profile from the current turn:
1. call `list_image_profiles`
2. choose the smallest profile that fits the task
3. use `generate_image` for first composition
4. once composition is correct, prefer `edit_image` for narrow changes

Default bias:
- first pass -> `draft`
- final-fidelity pass -> `quality`
- typography / text inside image -> `text_heavy`
- local corrections -> `edit`
- style transfer -> `style_transfer`
- recurring character identity -> `character_consistency`
- balanced transparent background / cutout -> `transparent_bg`
- cheaper/faster transparent draft -> `transparent_bg_fast`
- higher-fidelity isolated asset -> `cutout`

## Open only what you need

Always useful:
- `references/tool-surface.md`

Read when needed:
- `references/profile-selection.md` when choosing between profiles
- `references/prompting-patterns.md` when the prompt quality is the bottleneck
- `references/reference-images.md` when using refs or doing edits / style transfer / identity preservation

## Workflow

### 1. Choose the profile before reaching for a raw model id

Prefer the curated profile surface first. Use explicit `model` override only when:
- the user asked for a specific model,
- the profile is close but not exact,
- you are doing a bounded comparison or recovery move.

### 2. Generate first, then narrow by editing

Strong default loop:
1. `generate_image` -> get the composition / framing / rough style right
2. inspect result
3. `edit_image` -> make one narrow change at a time

Do not keep re-generating from scratch once the composition is already good.

### 3. Keep prompts structured, not magical

Good prompt shape is usually:
- subject
- style / medium
- composition / framing
- lighting / mood
- important details
- explicit constraints

See `references/prompting-patterns.md`.

### 4. Treat references as typed guidance

Do not send a pile of images without roles.
Use `reference_images=[{path, role}]` with roles like:
- `style`
- `subject`
- `object`
- `character`
- `layout`

For edits, `input_path` is the only editable base image; refs are guidance only.

### 5. Use GPT-image for true transparent backgrounds

In the current repo truth, transparent background generation is **not** a Gemini-family job.
If the user wants:
- transparent background
- alpha channel
- clean cutout / isolated asset

prefer one of these:
- `transparent_bg` for balanced quality
- `transparent_bg_fast` for cheap drafts
- `cutout` for higher-fidelity final isolated assets

## Common traps

- jumping straight to raw model ids when a profile already fits
- giant prompt with 20 demands instead of a draft -> edit loop
- re-generating from scratch when only one detail is wrong
- sending reference images without roles
- using `quality` too early, before composition is proven
- using `draft` for text-heavy final assets
- trying to get a real transparent background from Gemini-family image routes
- forgetting that the deliverable is the saved file path, not just the model response
