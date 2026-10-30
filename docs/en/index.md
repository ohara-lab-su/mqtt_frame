# mqtt_frame

MQTT-based device communication without MQTT dependencies in device classes.

## Semantics

- Unicast `call(device, method, ...)`: returns one result or raises `RpcError`/`RpcTimeout`.
- Multicast `multicast(group, method, ..., expected={...})`: collects responses until all expected devices respond or the deadline expires.
- Without `expected`, multicast collects until the deadline and cannot prove completeness.
- Events use `publish_event(name, value)` and `subscribe(device, name, callback)`.

## Limitations

QoS 1 can redeliver requests; **duplicate execution is not prevented**. MQTT delivery acknowledgement does not imply successful device execution. Do not use this implementation for safety interlocks. Authorization, control ownership and audit logging require deployment-specific design. Only JSON-serializable values are supported. Synchronous API only.

See [README](../../README.md) for examples.
