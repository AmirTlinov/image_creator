from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from image_creator.service import generate_image_artifact


def build_server() -> FastMCP:
    server = FastMCP("image-creator")

    @server.tool()
    async def generate_image(
        prompt: str,
        provider: str = "openrouter",
        model: str = "",
        out_dir: str = "",
        aspect_ratio: str = "1:1",
        image_size: str = "",
        output_name: str = "",
    ) -> str:
        """Generate an image, save it to disk, and return JSON with the final file path."""
        result = await generate_image_artifact(
            prompt=prompt,
            provider=provider,
            model=model or None,
            out_dir=out_dir or None,
            aspect_ratio=aspect_ratio or None,
            image_size=image_size or None,
            output_name=output_name or None,
        )
        return result.to_json()

    return server


mcp = build_server()


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
