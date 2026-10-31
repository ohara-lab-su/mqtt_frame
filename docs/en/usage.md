# Usage and examples


### Installation and broker startup

From the repository root (Python 3.10+):

```bash
python -m pip install .
```

Both `paho-mqtt` and the Python broker `amqtt` are installed as standard dependencies. **Installation does not automatically start the broker.** Open terminal 1 and run:

```bash
python examples/start_broker.py
```

This runs the bundled broker on `127.0.0.1:1883`. You can alternatively use `mqtt-frame-broker`, but do not run both at once. Stop it with Ctrl+C.

### Single-device RPC

In terminal 2:

```bash
python examples/server.py
```

In terminal 3:

```bash
python examples/client.py
```

The client invokes `move(100.0)` and `get_position()` on `motor1`. The `Motor` class contains no MQTT code.

### One-to-many method delivery

Stop the single-device server, but leave the broker running. In two separate terminals:

```bash
python examples/group_server.py motor1
```

```bash
python examples/group_server.py motor2
```

Once both servers have subscribed, run in a fourth terminal:

```bash
python examples/group_client.py
```

Both servers should print their `move(100.0)` execution. Group delivery does **not** aggregate responses or guarantee device execution. QoS 1 may redeliver commands.

### Independent Pub/Sub

```bash
python examples/broadcast.py
```

This publishes to `lab/motors/command`, which the example device servers do not subscribe to. The default broker allows anonymous local connections and must not be exposed to untrusted networks.
