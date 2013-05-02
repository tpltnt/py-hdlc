import sys
sys.path.append('../py-hdlc')
import pytest
from hdlc import BaseFrame


@pytest.fixture(scope="module")
def chunk1():
    """create a minimal/empty 'all station' basechunk with valid flags"""
    return b'\x7e\xff\x00\x00\x7e'


@pytest.fixture(scope="module")
def chunk2():
    """create a minimal/empty 'no station' basechunk with valid flags"""
    return b'\x7e\x00\x00\x00\x7e'


@pytest.fixture(scope="module")
def chunk3():
    """basic 2byte address field basechunk"""
    return b'\x7e\xf8\x01\x00\x7e'
