import os
import pytest
import requests
from unittest.mock import patch, Mock

from convertir_link_image import convert_link_to_image


def test_creation():
    converter = convert_link_to_image("https://example.com/image.jpg")

    assert converter.url == "https://example.com/image.jpg"
    assert converter.image_name == ""
    assert converter.image_code == b""


def test_convert_link_image():
    # Petite image JPEG valide
    image_data = (
        b"\xff\xd8\xff\xe0"
        b"\x00\x10JFIF\x00\x01\x01"
        b"\x00\x00\x01\x00\x01\x00\x00"
        b"\xff\xd9"
    )

    response = Mock()
    response.content = image_data

    with patch(
        "convertir_link_image.requests.get",
        return_value=response
    ):
        converter = convert_link_to_image(
            "https://example.com/image.jpg"
        )

        image_path = converter.convert_link_image()

    assert image_path != ""
    assert converter.image_name == image_path
    assert converter.image_code == image_data

    assert os.path.isfile(image_path)

    converter.delete_image_temp()


def test_convert_link_image_enregistre_le_fichier():
    image_data = b"contenu_image"

    response = Mock()
    response.content = image_data

    with patch(
        "convertir_link_image.requests.get",
        return_value=response
    ):
        converter = convert_link_to_image(
            "https://example.com/image.jpg"
        )

        image_path = converter.convert_link_image()

    assert os.path.exists(image_path)

    with open(image_path, "rb") as file:
        contenu = file.read()

    assert contenu == image_data

    converter.delete_image_temp()


def test_delete_image_temp():
    image_data = b"test"

    response = Mock()
    response.content = image_data

    with patch(
        "convertir_link_image.requests.get",
        return_value=response
    ):
        converter = convert_link_to_image(
            "https://example.com/image.jpg"
        )

        image_path = converter.convert_link_image()

    assert os.path.exists(image_path)

    converter.delete_image_temp()

    assert not os.path.exists(image_path)
    assert converter.image_name == ""


def test_delete_image_temp_sans_fichier():
    converter = convert_link_to_image(
        "https://example.com/image.jpg"
    )

    converter.delete_image_temp()

    assert converter.image_name == ""


def test_is_valid_image():
    # Une vraie petite image créée avec Pillow
    from PIL import Image

    image = Image.new("RGB", (10, 10), "white")

    converter = convert_link_to_image(
        "https://example.com/image.jpg"
    )

    # On crée un fichier temporaire
    with pytest.MonkeyPatch.context() as mp:
        import tempfile

        temp_file = tempfile.NamedTemporaryFile(
            suffix=".jpg",
            delete=False
        )

        image.save(temp_file, format="JPEG")
        temp_file.close()

        converter.image_name = temp_file.name

        assert converter.is_valid_image() is True

        os.remove(temp_file.name)


def test_is_valid_image_fausse_image(tmp_path):
    converter = convert_link_to_image(
        "https://example.com/image.jpg"
    )

    fake_image = tmp_path / "fake.jpg"
    fake_image.write_bytes(b"ceci nest pas une image")

    converter.image_name = str(fake_image)

    assert converter.is_valid_image() is False


def test_is_valid_image_fichier_inexistant():
    converter = convert_link_to_image(
        "https://example.com/image.jpg"
    )

    converter.image_name = "fichier_qui_nexiste_pas.jpg"

    assert converter.is_valid_image() is False