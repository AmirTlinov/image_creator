from image_creator.storage import save_image_bytes


def test_save_image_bytes_uses_mime_extension(tmp_path):
    path = save_image_bytes(b"png-bytes", "image/png", tmp_path)

    assert path.exists()
    assert path.suffix == ".png"
    assert path.read_bytes() == b"png-bytes"


def test_save_image_bytes_sanitizes_output_name(tmp_path):
    path = save_image_bytes(b"webp-bytes", "image/webp", tmp_path, "../poster")

    assert path.parent == tmp_path.resolve()
    assert path.name == "poster.webp"
    assert path.read_bytes() == b"webp-bytes"
