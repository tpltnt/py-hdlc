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


def test_parse_address_too_short_input(baseframe):
    with pytest.raises(ValueError):
        baseframe.parse_address(bytes(2))
