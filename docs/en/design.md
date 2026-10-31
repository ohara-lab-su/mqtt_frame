# Design and limitations

- Device classes are independent of MQTT; method dispatch is dynamic.
- Native Pub/Sub is independent of RPC. Fan-out does not require response aggregation.
- Multiple clients can use one server with per-client reply topics.
- Multiple servers can subscribe to a common topic; `DeviceServer(groups=...)` and `GroupPublisher` provide group request delivery; multi-server response aggregation is not implemented.
- Properties, coroutine methods, binary/custom serialization, device-specific typing stubs, and duplicate execution prevention are not implemented.
- QoS 1 does not guarantee exactly-once command execution. Do not use for safety interlocks.
- Compatibility with existing grpc_frame and ese774_frame source has not been verified.
