import sys
sys.path.append('../py-hdlc/hdlc')
import pytest
from IFrame import IFrame


def test_plain_init():
    foo = IFrame()


def test_parse_address1():
    """test for rejecting strings"""
    iframe = IFrame()
    with pytest.raises(TypeError):
        iframe.parse_address('test')


def test_parse_address2():
    """test for rejecting float input"""
    iframe = IFrame()
    with pytest.raises(TypeError):
        iframe.parse_address(2.3)


def test_parse_address3():
    """test for too short bytearray """
    iframe = IFrame()
    with pytest.raises(TypeError):
        iframe.parse_address(bytearray(1))


def test_parse_address4():
    """stripped input: just two zero-bytes"""
    iframe = IFrame()
    with pytest.raises(ValueError):
        iframe.parse_address(bytes(2))


#def test_parse_address_too_short_input2():
#    """unstripped input: just four zero-bytes"""
#    iframe = IFrame()
#    with pytest.raises(ValueError):
#        iframe.parse_address(bytes(4))


def test_parse_address5():
    """unstripped input, 4 bytes, valid opening and closing flags"""
    iframe = IFrame()
    with pytest.raises(ValueError):
        iframe.parse_address(b'\x7e\x00\x00\x7e')


def test_parse_address6():
    """unstripped input, 4 bytes, invalid opening flags"""
    iframe = IFrame()
    with pytest.raises(ValueError):
        iframe.parse_address(b'\x23\x00\x00\x7e')


def test_parse_address7():
    """unstripped input, 4 bytes, invalid closing flags"""
    iframe = IFrame()
    with pytest.raises(ValueError):
        iframe.parse_address(b'\x7e\x00\x00\x42')


#def test_parse_address8(chunk3):
#    """unstripped input, 5 bytes, 2byte address
#    iframe only allows 8 bits
#    """
#    iframe = IFrame()
#    with pytest.raises(ValueError):
#        iframe.parse_address(chunk3)


def test_parse_address9(chunk4):
    """parse I-frame control field with 1 byte address"""
    iframe = IFrame()
    iframe.parse_address(chunk4)


def test_is_allstation1(chunk1):
    """test frame generated with unicast/allstation address for having one"""
    iframe = IFrame()
    iframe.parse_address(chunk1)
    assert iframe.is_allstation() is True


def test_is_allstation2():
    """vanilla object should not have an allstation address assigned"""
    iframe = IFrame()
    assert iframe.is_allstation() is False


def test_is_allstation3(chunk2):
    """"given a no-station address, testing is_allstation should yield False"""
    iframe = IFrame()
    iframe.parse_address(chunk2)
    assert iframe.is_allstation() is False


def test_is_nostation1():
    """'no station' should be the default address for a base frame."""
    iframe = IFrame()
    assert iframe.is_nostation() is True


def test_is_nostation2(chunk1):
    """parsing a all-station address should return False on is_nostation()"""
    iframe = IFrame()
    iframe.parse_address(chunk1)
    assert iframe.is_nostation() is False


def test_is_nostation3(chunk2):
    """parsing a no-station address should return True in is_nostation()"""
    iframe = IFrame()
    iframe.parse_address(chunk2)
    assert iframe.is_nostation() is True


def test_set_address1():
    """setting an arbitary 8bit address with clear MSB should work."""
    iframe = IFrame()
    iframe.set_address(bytes([42]))


def test_set_address2():
    """giving int as address should fail"""
    iframe = IFrame()
    with pytest.raises(TypeError):
        iframe.set_address(42)


def test_set_address3():
    """giving string as address should fail"""
    iframe = IFrame()
    with pytest.raises(TypeError):
        iframe.set_address('23')


def test_set_address4():
    """setting 'all station' should work"""
    iframe = IFrame()
    iframe.set_address(bytes([255]))
    assert iframe.is_allstation() is True


def test_get_address0():
    """setting and retrieving an 8bit address on a iframe."""
    iframe = IFrame()
    iframe.set_address(bytes([42]))
    assert bytes([42]) == iframe.get_address()


def test_get_address1():
    """test for returning bytes()"""
    iframe = IFrame()
    assert isinstance(iframe.get_address(), bytes)


def test_set_control0():
    """test for passing a bytes instance."""
    iframe = IFrame()
    iframe.set_control(bytes([42]))


def test_set_control1():
    """test for passing Bytes array."""
    iframe = IFrame()
    with pytest.raises(TypeError):
        iframe.set_control(bytearray(1))


def test_set_control2():
    """test for setting 24 control bits"""
    iframe = IFrame()
    iframe.set_control(bytes([5, 23, 42]))


def test_get_control0():
    """test for retrieving set control field."""
    iframe = IFrame()
    iframe.set_control(bytes([42]))
    assert bytes([42]) == iframe.get_control()


def test_get_control1():
    """test for retrieving correct type"""
    iframe = IFrame()
    assert isinstance(iframe.get_control(), bytes)


def test_is_IFrame0():
    """set I-frame bit and control for it."""
    iframe = IFrame()
    iframe.set_control(bytes([42]))
    assert iframe.is_IFrame() is True


def test_is_IFrame1():
    """test non-I-frame for being one."""
    iframe = IFrame()
    iframe.set_control(bytes([128]))
    assert iframe.is_IFrame() is False


def test_get_receive_sequence_number0():
    """test for extracting max number"""
    iframe = IFrame()
    # 119 = 0x77 = 01110111
    iframe.set_control(bytes([119]))
    assert 7 == iframe.get_receive_sequence_number()


def test_get_receive_sequence_number1():
    """test for extracting min. number"""
    iframe = IFrame()
    iframe.set_control(bytes([112]))
    assert 0 == iframe.get_receive_sequence_number()


def test_get_receive_sequence_number2():
    """test for correct return type"""
    iframe = IFrame()
    assert isinstance(iframe.get_receive_sequence_number(), int)
