# Profile selection

Prefer the smallest profile that matches the job.

## `draft`

Use for:
- fast exploration
- first composition pass
- broad ideation

Avoid when:
- final typography quality matters
- you already know this is a final brand-facing asset

## `quality`

Use for:
- final fidelity
- premium visuals
- polished product / marketing assets

Practical move:
- use only after the composition is already right

## `text_heavy`

Use for:
- images with meaningful text inside
- layout-critical copy
- logos / wordmarks / promo cards

Default bias:
- if text accuracy matters more than speed, choose this

## `edit`

Use for:
- small corrections
- object insertion / removal
- color tweaks
- preserving composition while changing one thing

## `style_transfer`

Use for:
- same composition, different rendering style
- taking one base image and one style reference

## `character_consistency`

Use for:
- recurring character identity
- consistent face / costume / silhouette across variants

## `transparent_bg`

Use for:
- transparent background
- alpha-channel output
- clean product cutouts
- isolated assets for composition in other tools

Important:
- this is the GPT-image path
- do not try to solve this with Gemini-family image routes

## `transparent_bg_fast`

Use for:
- cheap transparent drafts
- fast isolated icons / stickers / rough assets

Use this when:
- you need alpha channel
- speed matters more than final edge fidelity

## `cutout`

Use for:
- premium isolated assets
- product cutouts
- cleaner final edges for production use

Use this when:
- alpha channel matters
- the asset is closer to final than to draft
- you would otherwise be tempted to use `transparent_bg` + many retries

## Raw model override

Only use explicit `model=` when:
- the user asked for it
- you are comparing two concrete models
- a curated profile is close but not enough
