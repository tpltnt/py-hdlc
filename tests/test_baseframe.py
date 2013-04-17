import sys
sys.path.append('../py-hdlc')
import pytest
from hdlc import HDLCBaseFrame


def test_plain_init():
    foo = HDLCBaseFrame()


def test_parse_address_string_input(baseframe):
    with pytest.raises(TypeError):
        baseframe.parse_address('test')


def test_parse_address_float_input(baseframe):
    with pytest.raises(TypeError):
        baseframe.parse_address(2.3)


def test_parse_address_bytearray_input(baseframe):
    with pytest.raises(TypeError):
        baseframe.parse_address(bytearray(1))


def test_parse_address_too_short_input1(baseframe):
    """stripped input: just two zero-bytes"""
    with pytest.raises(ValueError):
        baseframe.parse_address(bytes(2))


def test_parse_address_too_short_input2(baseframe):
    """unstripped input: just four zero-bytes"""
    with pytest.raises(ValueError):
        baseframe.parse_address(bytes(4))


def test_parse_address_too_short_input3(baseframe):
    """unstripped input, 4 bytes, valid opening and closing flags"""
    with pytest.raises(ValueError):
        baseframe.parse_address(b'\x7e\x00\x00\x7e')


def test_parse_address_too_short_input4(baseframe):
    """unstripped input, 4 bytes, invalid opening flags"""
    with pytest.raises(ValueError):
        baseframe.parse_address(b'\x23\x00\x00\x7e')


def test_parse_address_too_short_input5(baseframe):
    """unstripped input, 4 bytes, invalid closing flags"""
    with pytest.raises(ValueError):
        baseframe.parse_address(b'\x7e\x00\x00\x42')


def test_is_allstation(baseframe, chunk1):
    """test frame generated with unicast/allstattion address for having one"""
    baseframe.parse_address(chunk1)
    assert baseframe.is_allstation() is True
