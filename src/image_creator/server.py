from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from image_creator.service import edit_image_artifact, generate_image_artifact, list_image_profiles as get_image_profiles


def build_server() -> FastMCP:
    server = FastMCP("image-creator")

    @server.tool()
    async def generate_image(
        prompt: str,
        provider: str = "openrouter",
        model: str = "",
        profile: str = "",
        out_dir: str = "",
        aspect_ratio: str = "1:1",
        image_size: str = "",
        negative_prompt: str = "",
        reference_images: list[dict[str, str]] | None = None,
        output_name: str = "",
    ) -> dict[str, str]:
        """Generate an image, save it to disk, and return a structured result with the final file path."""
        result = await generate_image_artifact(
            prompt=prompt,
            provider=provider,
            model=model or None,
            profile=profile or None,
            out_dir=out_dir or None,
            aspect_ratio=aspect_ratio or None,
            image_size=image_size or None,
            negative_prompt=negative_prompt or None,
            reference_images=reference_images,
            output_name=output_name or None,
        )
        return result.to_dict()

    @server.tool()
    async def edit_image(
        input_path: str,
        prompt: str,
        provider: str = "openrouter",
        model: str = "",
        profile: str = "",
        out_dir: str = "",
        aspect_ratio: str = "1:1",
        image_size: str = "",
        negative_prompt: str = "",
        reference_images: list[dict[str, str]] | None = None,
        output_name: str = "",
    ) -> dict[str, str]:
        """Edit an existing local image, save the new image to disk, and return a structured result."""
        result = await edit_image_artifact(
            input_path=input_path,
            prompt=prompt,
            provider=provider,
            model=model or None,
            profile=profile or None,
            out_dir=out_dir or None,
            aspect_ratio=aspect_ratio or None,
            image_size=image_size or None,
            negative_prompt=negative_prompt or None,
            reference_images=reference_images,
            output_name=output_name or None,
        )
        return result.to_dict()

    @server.tool()
    def list_image_profiles() -> dict[str, list[dict[str, object]]]:
        """Return curated image-generation profiles so the agent can choose a model path cheaply."""
        return get_image_profiles()

    return server


mcp = build_server()


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
