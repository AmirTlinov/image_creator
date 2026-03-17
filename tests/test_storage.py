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


def test_save_image_bytes_avoids_overwriting_existing_named_output(tmp_path):
    first = save_image_bytes(b"first", "image/png", tmp_path, "poster")
    second = save_image_bytes(b"second", "image/png", tmp_path, "poster")

    assert first.name == "poster.png"
    assert second.name == "poster-2.png"
    assert first.read_bytes() == b"first"
    assert second.read_bytes() == b"second"
