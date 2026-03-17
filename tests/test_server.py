from image_creator.server import build_server


def test_build_server_returns_instance():
    server = build_server()

    assert server is not None
