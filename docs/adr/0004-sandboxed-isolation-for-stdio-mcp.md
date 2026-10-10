# Sandboxed Isolation for STDIO MCP Subprocesses

We evaluated running STDIO Model Context Protocol (MCP) server processes directly on the FastAPI / SAQ host backend versus isolating them in containerized sandboxes. We decided that all STDIO MCP processes must execute inside isolated micro-containers (Docker or E2B) with encrypted credential injection, strictly barring subprocess execution on the host backend. This prevents untrusted external tool servers or compromised package ecosystems from compromising host secrets or accessing private cluster networks.
