"""motorsグループへ同一メソッド呼び出しを配信する。"""
from mqtt_frame import GroupPublisher

client = GroupPublisher().start()
try:
    info = client.call("motors", "move", 100.0)
    info.wait_for_publish()
    print("Brokerへのpublish完了。各デバイスの実行完了は保証しません。")
finally:
    client.close()
