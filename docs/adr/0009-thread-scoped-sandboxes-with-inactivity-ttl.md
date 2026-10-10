# Thread-Scoped Sandboxes with Inactivity TTL

We evaluated whether to create disposable sandboxes per tool call, maintain permanent container daemons, or scope sandboxes to conversations. We decided that E2B execution sandboxes are scoped to a Thread and automatically destroyed after 15 minutes of inactivity or explicit thread closure. This preserves filesystem state across multi-turn developer workflows (e.g. cloning a repo, modifying files, running tests) while strictly capping cloud compute expenditure and preventing abandoned runner processes.
