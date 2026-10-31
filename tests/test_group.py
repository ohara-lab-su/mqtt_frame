from unittest.mock import Mock, patch
from mqtt_frame.group import GroupPublisher
from mqtt_frame.protocol import loads

def test_group_publish():
    with patch("mqtt_frame.group.Connection") as factory:
        conn = factory.return_value
        publisher = GroupPublisher(namespace="devices")
        publisher.call("motors", "move", 10)
        topic, payload = conn.publish.call_args.args
        assert topic == "devices/_groups/motors/rpc/request"
        assert loads(payload)["method"] == "move"
        assert loads(payload)["args"] == [10]
