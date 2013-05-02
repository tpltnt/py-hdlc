import sys
sys.path.append('../py-hdlc')
import pytest
from hdlc import BaseFrame


def test_plain_init():
    foo = BaseFrame()


def test_parse_address_string_input():
    baseframe = BaseFrame()
    with pytest.raises(TypeError):
        baseframe.parse_address('test')


def test_parse_address_float_input():
    baseframe = BaseFrame()
    with pytest.raises(TypeError):
        baseframe.parse_address(2.3)


def test_parse_address_bytearray_input():
    baseframe = BaseFrame()
    with pytest.raises(TypeError):
        baseframe.parse_address(bytearray(1))


def test_parse_address_too_short_input1():
    """stripped input: just two zero-bytes"""
    baseframe = BaseFrame()
    with pytest.raises(ValueError):
        baseframe.parse_address(bytes(2))


#def test_parse_address_too_short_input2():
#    """unstripped input: just four zero-bytes"""
#    baseframe = BaseFrame()
#    with pytest.raises(ValueError):
#        baseframe.parse_address(bytes(4))


def test_parse_address_too_short_input3():
    """unstripped input, 4 bytes, valid opening and closing flags"""
    baseframe = BaseFrame()
    with pytest.raises(ValueError):
        baseframe.parse_address(b'\x7e\x00\x00\x7e')


def test_parse_address_too_short_input4():
    """unstripped input, 4 bytes, invalid opening flags"""
    baseframe = BaseFrame()
    with pytest.raises(ValueError):
        baseframe.parse_address(b'\x23\x00\x00\x7e')


def test_parse_address_too_short_input5():
    """unstripped input, 4 bytes, invalid closing flags"""
    baseframe = BaseFrame()
    with pytest.raises(ValueError):
        baseframe.parse_address(b'\x7e\x00\x00\x42')


def test_is_allstation1(chunk1):
    """test frame generated with unicast/allstation address for having one"""
    baseframe = BaseFrame()
    baseframe.parse_address(chunk1)
    assert baseframe.is_allstation() is True


def test_is_allstation2():
    """vanilla object should not have an allstation address assigned"""
    baseframe = BaseFrame()
    assert baseframe.is_allstation() is False


def test_is_allstation3(chunk2):
    """"given a no-station address, testing is_allstation should yield False"""
    baseframe = BaseFrame()
    baseframe.parse_address(chunk2)
    assert baseframe.is_allstation() is False


def test_is_nostation1():
    """'no station' should be the default address for a base frame."""
    baseframe = BaseFrame()
    assert baseframe.is_nostation() is True


def test_is_nostation2(chunk1):
    """parsing a all-station address should return False on is_nostation()"""
    baseframe = BaseFrame()
    baseframe.parse_address(chunk1)
    assert baseframe.is_nostation() is False


def test_is_nostation3(chunk2):
    """parsing a no-station address should return True in is_nostation()"""
    baseframe = BaseFrame()
    baseframe.parse_address(chunk2)
    assert baseframe.is_nostation() is True


def test_set_address1():
    """setting an arbitary 8bit address with clear MSB should work."""
    baseframe = BaseFrame()
    baseframe.set_address(bytes([42]))


def test_set_address2():
    """giving int as address should fail"""
    baseframe = BaseFrame()
    with pytest.raises(TypeError):
        baseframe.set_address(42)


def test_set_address3():
    """giving string as address should fail"""
    baseframe = BaseFrame()
    with pytest.raises(TypeError):
        baseframe.set_address('23')


def test_set_address4():
    """setting 'all station' should work"""
    baseframe = BaseFrame()
    baseframe.set_address(bytes([255]))
    assert baseframe.is_allstation() is True


def test_set_address5():
    """Setting a 16bit address on base frame should fail.
    The ISO standard only allows 8bit for baseframe."""
    baseframe = BaseFrame()
    with pytest.raises(ValueError):
        baseframe.set_address(bytes([23, 42]))


def test_get_address0():
    """setting and retrieving an 8bit address on a baseframe."""
    baseframe = BaseFrame()
    baseframe.set_address(bytes([42]))
    assert bytes([42]) == baseframe.get_address()


def test_get_address1():
    """test for returning bytes()"""
    baseframe = BaseFrame()
    assert isinstance(baseframe.get_address(), bytes)


def test_set_control0():
    """test for passing a bytes instance."""
    baseframe = BaseFrame()
    baseframe.set_control(bytes([42]))


def test_set_control1():
    """test for passing Bytes array."""
    baseframe = BaseFrame()
    with pytest.raises(TypeError):
        baseframe.set_control(bytearray(1))


def test_set_control2():
    """test for setting 24 bits"""
    baseframe = BaseFrame()
    with pytest.raises(ValueError):
        baseframe.set_control(bytes([5, 23, 42]))


def test_get_control0():
    """test for retrieving set control field."""
    baseframe = BaseFrame()
    baseframe.set_control(bytes([42]))
    assert bytes([42]) == baseframe.get_control()


def test_get_control1():
    """test for retrieving correct type"""
    baseframe = BaseFrame()
    assert isinstance(baseframe.get_control(), bytes)


def test_is_Iframe0():
    """set I-frame bit and control for it."""
    baseframe = BaseFrame()
    baseframe.set_control(bytes([42]))
    assert baseframe.is_Iframe() is True


def test_is_Iframe1():
    """test non-I-frame for being one."""
    baseframe = BaseFrame()
    baseframe.set_control(bytes([128]))
    assert baseframe.is_Iframe() is False


def test_get_receive_sequence_number0():
    """test for extracting max number"""
    baseframe = BaseFrame()
    # 119 = 0x77 = 01110111
    baseframe.set_control(bytes([119]))
    assert 7 == baseframe.get_receive_sequence_number()


def test_get_receive_sequence_number1():
    """test for extracting min. number"""
    baseframe = BaseFrame()
    baseframe.set_control(bytes([112]))
    assert 0 == baseframe.get_receive_sequence_number()


def test_get_receive_sequence_number2():
    """test for correct return type"""
    baseframe = BaseFrame()
    assert isinstance(baseframe.get_receive_sequence_number(), int)
