# Resilient Event Replay via Redis Streams

We evaluated ephemeral Redis Pub/Sub channels versus Redis Streams with offset replay for SSE communication. We decided that all task execution events are published to Redis Streams (`task:{id}:events`) and read by the SSE endpoint using standard `Last-Event-ID` headers. This guarantees that if a client temporarily disconnects during a long-running task, it automatically receives all missed intermediate steps, tool calls, and approval requests upon reconnecting without state corruption or stuck UI spinners.
