import sys
sys.path.append('../py-hdlc')
import pytest
from hdlc import HDLCBaseFrame


def test_plain_init():
    foo = HDLCBaseFrame()


def test_parse_address_string_input():
    baseframe = HDLCBaseFrame()
    with pytest.raises(TypeError):
        baseframe.parse_address('test')


def test_parse_address_float_input():
    baseframe = HDLCBaseFrame()
    with pytest.raises(TypeError):
        baseframe.parse_address(2.3)


def test_parse_address_bytearray_input():
    baseframe = HDLCBaseFrame()
    with pytest.raises(TypeError):
        baseframe.parse_address(bytearray(1))


def test_parse_address_too_short_input1():
    """stripped input: just two zero-bytes"""
    baseframe = HDLCBaseFrame()
    with pytest.raises(ValueError):
        baseframe.parse_address(bytes(2))


#def test_parse_address_too_short_input2():
#    """unstripped input: just four zero-bytes"""
#    baseframe = HDLCBaseFrame()
#    with pytest.raises(ValueError):
#        baseframe.parse_address(bytes(4))


def test_parse_address_too_short_input3():
    """unstripped input, 4 bytes, valid opening and closing flags"""
    baseframe = HDLCBaseFrame()
    with pytest.raises(ValueError):
        baseframe.parse_address(b'\x7e\x00\x00\x7e')


def test_parse_address_too_short_input4():
    """unstripped input, 4 bytes, invalid opening flags"""
    baseframe = HDLCBaseFrame()
    with pytest.raises(ValueError):
        baseframe.parse_address(b'\x23\x00\x00\x7e')


def test_parse_address_too_short_input5():
    """unstripped input, 4 bytes, invalid closing flags"""
    baseframe = HDLCBaseFrame()
    with pytest.raises(ValueError):
        baseframe.parse_address(b'\x7e\x00\x00\x42')


def test_is_allstation1(chunk1):
    """test frame generated with unicast/allstation address for having one"""
    baseframe = HDLCBaseFrame()
    baseframe.parse_address(chunk1)
    assert baseframe.is_allstation() is True


def test_is_allstation2():
    """vanilla object should not have an allstation address assigned"""
    baseframe = HDLCBaseFrame()
    assert baseframe.is_allstation() is False


def test_is_allstation3(chunk2):
    """"given a no-station address, testing is_allstation should yield False"""
    baseframe = HDLCBaseFrame()
    baseframe.parse_address(chunk2)
    assert baseframe.is_allstation() is False


def test_is_nostation1():
    """'no station' should be the default address for a base frame."""
    baseframe = HDLCBaseFrame()
    assert baseframe.is_nostation() is True


def test_is_nostation2(chunk1):
    """parsing a all-station address should return False on is_nostation()"""
    baseframe = HDLCBaseFrame()
    baseframe.parse_address(chunk1)
    assert baseframe.is_nostation() is False


def test_is_nostation3(chunk2):
    """parsing a no-station address should return True in is_nostation()"""
    baseframe = HDLCBaseFrame()
    baseframe.parse_address(chunk2)
    assert baseframe.is_nostation() is True


def test_set_address1():
    """setting an arbitary 8bit address with clear MSB should work."""
    baseframe = HDLCBaseFrame()
    baseframe.set_address(bytes([42]))


def test_set_address2():
    """giving int as address should fail"""
    baseframe = HDLCBaseFrame()
    with pytest.raises(TypeError):
        baseframe.set_address(42)


def test_set_address3():
    """giving string as address should fail"""
    baseframe = HDLCBaseFrame()
    with pytest.raises(TypeError):
        baseframe.set_address('23')


def test_set_address4():
    """setting 'all station' should work"""
    baseframe = HDLCBaseFrame()
    baseframe.set_address(bytes([255]))
    assert baseframe.is_allstation() is True
