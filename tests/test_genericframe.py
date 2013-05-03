import sys
sys.path.append('../py-hdlc/hdlc')
import pytest
from GenericFrame import GenericFrame


def test_plain_init():
    foo = GenericFrame()


def test_parse_address1():
    """test for rejecting strings"""
    genericframe = GenericFrame()
    with pytest.raises(TypeError):
        genericframe.parse_address('test')


def test_parse_address2():
    """test for rejecting float input"""
    genericframe = GenericFrame()
    with pytest.raises(TypeError):
        genericframe.parse_address(2.3)


def test_parse_address3():
    """test for too short bytearray """
    genericframe = GenericFrame()
    with pytest.raises(TypeError):
        genericframe.parse_address(bytearray(1))


def test_parse_address4():
    """stripped input: just two zero-bytes"""
    genericframe = GenericFrame()
    with pytest.raises(ValueError):
        genericframe.parse_address(bytes(2))


def test_parse_address5():
    """unstripped input, 4 bytes, valid opening and closing flags"""
    genericframe = GenericFrame()
    with pytest.raises(ValueError):
        genericframe.parse_address(b'\x7e\x00\x00\x7e')


def test_parse_address6():
    """unstripped input, 4 bytes, invalid opening flags"""
    genericframe = GenericFrame()
    with pytest.raises(ValueError):
        genericframe.parse_address(b'\x23\x00\x00\x7e')


def test_parse_address7():
    """unstripped input, 4 bytes, invalid closing flags"""
    genericframe = GenericFrame()
    with pytest.raises(ValueError):
        genericframe.parse_address(b'\x7e\x00\x00\x42')


def test_parse_address9(chunk4):
    """parse I-frame control field with 1 byte address"""
    genericframe = GenericFrame()
    genericframe.parse_address(chunk4)


def test_is_allstation1(chunk1):
    """test frame generated with unicast/allstation address for having one"""
    genericframe = GenericFrame()
    genericframe.parse_address(chunk1)
    assert genericframe.is_allstation() is True


def test_is_allstation2():
    """vanilla object should not have an allstation address assigned"""
    genericframe = GenericFrame()
    assert genericframe.is_allstation() is False


def test_is_allstation3(chunk2):
    """"given a no-station address, testing is_allstation should yield False"""
    genericframe = GenericFrame()
    genericframe.parse_address(chunk2)
    assert genericframe.is_allstation() is False


def test_is_nostation1():
    """'no station' should be the default address for a base frame."""
    genericframe = GenericFrame()
    assert genericframe.is_nostation() is True


def test_is_nostation2(chunk1):
    """parsing a all-station address should return False on is_nostation()"""
    genericframe = GenericFrame()
    genericframe.parse_address(chunk1)
    assert genericframe.is_nostation() is False


def test_is_nostation3(chunk2):
    """parsing a no-station address should return True in is_nostation()"""
    genericframe = GenericFrame()
    genericframe.parse_address(chunk2)
    assert genericframe.is_nostation() is True


def test_set_address1():
    """setting an arbitary 8bit address with clear MSB should work."""
    genericframe = GenericFrame()
    genericframe.set_address(bytes([42]))


def test_set_address2():
    """giving int as address should fail"""
    genericframe = GenericFrame()
    with pytest.raises(TypeError):
        genericframe.set_address(42)


def test_set_address3():
    """giving string as address should fail"""
    genericframe = GenericFrame()
    with pytest.raises(TypeError):
        genericframe.set_address('23')


def test_set_address4():
    """setting 'all station' should work"""
    genericframe = GenericFrame()
    genericframe.set_address(bytes([255]))
    assert genericframe.is_allstation() is True


def test_set_address5():
    """Setting a 16bit address on base frame should fail.
    The ISO standard only allows 8bit for genericframe."""
    genericframe = GenericFrame()
    with pytest.raises(ValueError):
        genericframe.set_address(bytes([23, 42]))


def test_get_address0():
    """setting and retrieving an 8bit address on a genericframe."""
    genericframe = GenericFrame()
    genericframe.set_address(bytes([42]))
    assert bytes([42]) == genericframe.get_address()


def test_get_address1():
    """test for returning bytes()"""
    genericframe = GenericFrame()
    assert isinstance(genericframe.get_address(), bytes)


def test_set_control0():
    """test for passing a bytes instance."""
    genericframe = GenericFrame()
    genericframe.set_control(bytes([42]))


def test_set_control1():
    """test for passing Bytes array."""
    genericframe = GenericFrame()
    with pytest.raises(TypeError):
        genericframe.set_control(bytearray(1))


def test_set_control2():
    """test for setting 24 bits"""
    genericframe = GenericFrame()
    with pytest.raises(ValueError):
        genericframe.set_control(bytes([5, 23, 42]))


def test_get_control0():
    """test for retrieving set control field."""
    genericframe = GenericFrame()
    genericframe.set_control(bytes([42]))
    assert bytes([42]) == genericframe.get_control()


def test_get_control1():
    """test for retrieving correct type"""
    genericframe = GenericFrame()
    assert isinstance(genericframe.get_control(), bytes)


def test_is_IFrame0():
    """set I-frame bit and control for it."""
    genericframe = GenericFrame()
    genericframe.set_control(bytes([42]))
    assert genericframe.is_IFrame() is True


def test_is_IFrame1():
    """test non-I-frame for being one."""
    genericframe = GenericFrame()
    genericframe.set_control(bytes([128]))
    assert genericframe.is_IFrame() is False
