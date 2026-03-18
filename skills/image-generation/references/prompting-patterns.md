# Prompting patterns

The point is not to write longer prompts. The point is to write clearer prompts.

## Good generation shape

Keep this order when useful:
1. subject
2. style / medium
3. composition / framing
4. lighting / mood
5. key details
6. constraints

Example:

```text
Create a premium skincare jar hero image.
Style: clean photorealistic studio product photography.
Composition: centered jar, slight top-down angle, negative space around the object.
Lighting: soft studio lighting with gentle reflections.
Key details: matte white jar, minimal label, subtle shadow.
Constraints: no watermark, no extra objects, no text outside the label.
```

## Good edit shape

Use this structure:
- say what changes
- say what must stay unchanged
- say that the change must integrate naturally

Example:

```text
Change only the sunglasses.
Keep unchanged: banana shape, white background, flat illustration style, composition.
Make the sunglasses integrate naturally with the existing perspective and lighting.
```

## Negative prompt

Use `negative_prompt` only for things that really must be excluded.
Good examples:
- `no watermark`
- `no extra objects`
- `no text`
- `no cropped subject`

Do not stuff it with generic fear words.

## Efficient loop

Best practical loop:
1. `draft`
2. inspect
3. `edit` for narrow changes
4. `quality` only when the composition is already proven

## When to switch to `text_heavy`

Switch when the image contains meaningful text that must be legible and correct.

## When to switch to `quality`

Switch when:
- the user wants a final asset
- details / materials / polish matter more than speed
- the draft already solved the composition problem

## When to switch to transparent profiles

Use `transparent_bg` when the task is transparency / alpha channel / isolated asset and you want a balanced route.

Use `transparent_bg_fast` when the task is the same, but speed and cost matter more than edge fidelity.

Use `cutout` when the asset is closer to final delivery and edge quality matters.

Example transparent prompt:

```text
Create a clean isolated product cutout of a red sneaker.
Centered object, full silhouette visible.
No background elements, no shadow spill beyond the object.
```
