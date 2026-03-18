# Reference images

Reference images are powerful when they are typed.

## Roles

Supported roles:
- `style`
- `subject`
- `object`
- `character`
- `layout`

## How to think about them

- `style` -> how it should look
- `subject` -> what subject identity should feel like
- `object` -> a specific object or logo to preserve or inject
- `character` -> recurring character identity
- `layout` -> composition / placement inspiration

## For edits

In `edit_image`:
- `input_path` = editable base image
- `reference_images` = guidance only

That means the right mental model is:
- edit this image
- guided by these references

## Strong default shapes

### Style transfer

- `input_path` = base composition
- one `style` reference
- prompt says: keep composition, change rendering style

### Character consistency

- one or more `character` references
- prompt says what to preserve about identity
- use narrow edits rather than giant scene rewrites

### Object insertion

- base image to edit
- one `object` reference if needed
- prompt says where to place it and what must remain unchanged

## Limits

Current enforced limits:
- max 14 total refs
- max 4 `character`
- max 10 non-character refs

Stay well below the max unless the task truly needs it.
Usually 1-3 strong references beat a large heap of weak ones.

## Transparent background reminder

If the actual task is transparency / cutout, reference images are secondary.
The first move is selecting a transparent-background profile, because that capability is model-dependent.
