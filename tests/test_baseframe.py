import sys
sys.path.append('../py-hdlc')
import pytest
from hdlc import HDLCBaseFrame

def test_plain_init():
    foo = HDLCBaseFrame()
