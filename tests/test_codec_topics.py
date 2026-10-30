from mqtt_frame.codec import encode, decode
from mqtt_frame.topics import request, group, segment
import pytest

def test_json_roundtrip():
    assert decode(encode({'値': [1, True]})) == {'値': [1, True]}

def test_topics():
    assert request('mqtt_frame', 'motor1') == 'mqtt_frame/rpc/motor1/request'
    assert group('mqtt_frame', 'motors') == 'mqtt_frame/group/motors/request'
    with pytest.raises(ValueError): segment('bad/#')
