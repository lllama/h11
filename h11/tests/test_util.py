import re

import pytest

from .._util import *

def test_LocalProtocolError():
    try:
        raise LocalProtocolError("foo")
    except LocalProtocolError as e:
        assert str(e) == "foo"
        assert e.error_status_hint == 400

    try:
        raise LocalProtocolError("foo", error_status_hint=418)
    except LocalProtocolError as e:
        assert str(e) == "foo"
        assert e.error_status_hint == 418

def test_validate():
    my_re = re.compile(br"(?P<group1>[0-9]+)\.(?P<group2>[0-9]+)")
    with pytest.raises(LocalProtocolError):
        validate(my_re, b"0.")

    groups = validate(my_re, b"0.1")
    assert groups == {"group1": b"0", "group2": b"1"}

    # successful partial matches are an error - must match whole string
    with pytest.raises(LocalProtocolError):
        validate(my_re, b"0.1xx")
    with pytest.raises(LocalProtocolError):
        validate(my_re, b"0.1\n")

def test_Sentinel():
    S = Sentinel("S")
    assert repr(S) == "S"
    assert S == S
    assert S in {S}

def test_bytesify():
    assert bytesify(b"123") == b"123"
    assert bytesify(bytearray(b"123")) == b"123"
    assert bytesify("123") == b"123"

    with pytest.raises(UnicodeEncodeError):
        bytesify(u"\u1234")

    with pytest.raises(TypeError):
        bytesify(10)
