from typing import Union
import pytest
import numpy as np

from hub.codec import NumPy, Lz4, Zstd, JpegCodec, PngCodec

IMG_ARRAY_SHAPES = ((30, 30, 3), (2, 30, 30, 3), (30, 30, 1))
GENERIC_ARRAY_SHAPES = ((20, 1), (1, 20), ((60, 60)))
ARRAY_DTYPES = (
    "uint8",
    "uint16",
    "float16",
    "float32",
)
LZ4_ACCELERATIONS = (1, 50, 100)
ZSTD_LEVELS = (1, 11, 22)


def check_equals_decoded(
    actual_array: np.ndarray, codec: Union[PngCodec, NumPy, Lz4, Zstd, JpegCodec]
):
    bytes_ = codec.encode(actual_array)
    decoded_array = codec.decode(bytes_)
    assert (actual_array == decoded_array).all()


@pytest.mark.parametrize("from_config", [False, True])
@pytest.mark.parametrize("shape", IMG_ARRAY_SHAPES)
def test_png_codec(from_config: bool, shape: tuple) -> None:
    codec = PngCodec()
    if from_config:
        config = codec.get_config()
        codec = PngCodec.from_config(config)
    arr = np.ones(shape, dtype="uint8")
    check_equals_decoded(arr, codec)


@pytest.mark.parametrize("single_channel", [False, True])
def test_png_codec_config(single_channel: bool) -> None:
    codec = PngCodec(single_channel)
    config = codec.get_config()
    assert config["id"] == "png"
    assert config["single_channel"] == single_channel


@pytest.mark.parametrize("single_channel", [False, True])
def test_png_codec_single_channel(single_channel: bool) -> None:
    codec = PngCodec(single_channel)
    if single_channel:
        arr = np.ones((100, 100, 1), dtype="uint8")
    else:
        arr = np.ones((100, 100), dtype="uint8")
    check_equals_decoded(arr, codec)


@pytest.mark.parametrize("from_config", [False, True])
@pytest.mark.parametrize("shape", IMG_ARRAY_SHAPES)
def test_jpeg_codec(from_config: bool, shape: tuple) -> None:
    codec = JpegCodec()
    if from_config:
        config = codec.get_config()
        codec = JpegCodec.from_config(config)
    arr = np.ones(shape, dtype="uint8")
    check_equals_decoded(arr, codec)


@pytest.mark.parametrize("single_channel", [False, True])
def test_jpeg_codec_config(single_channel: bool) -> None:
    codec = JpegCodec(single_channel)
    config = codec.get_config()
    assert config["id"] == "jpeg"
    assert config["single_channel"] == single_channel


@pytest.mark.parametrize("single_channel", [False, True])
def test_jpeg_codec_single_channel(single_channel: bool) -> None:
    codec = JpegCodec(single_channel)
    if single_channel:
        arr = np.ones((100, 100, 1), dtype="uint8")
    else:
        arr = np.ones((100, 100), dtype="uint8")
    check_equals_decoded(arr, codec)


@pytest.mark.parametrize("acceleration", LZ4_ACCELERATIONS)
@pytest.mark.parametrize("shape", GENERIC_ARRAY_SHAPES)
def test_lz4(acceleration: int, shape: tuple) -> None:
    codec = Lz4(acceleration=acceleration)
    arr = np.random.rand(*shape)
    check_equals_decoded(arr, codec)


@pytest.mark.parametrize("shape", GENERIC_ARRAY_SHAPES)
def test_numpy(shape: tuple) -> None:
    codec = NumPy()
    arr = np.random.rand(*shape)
    check_equals_decoded(arr, codec)


@pytest.mark.parametrize("level", ZSTD_LEVELS)
@pytest.mark.parametrize("shape", GENERIC_ARRAY_SHAPES)
def test_zstd(level: int, shape: tuple) -> None:
    codec = Zstd(level=level)
    arr = np.random.rand(*shape)
    check_equals_decoded(arr, codec)