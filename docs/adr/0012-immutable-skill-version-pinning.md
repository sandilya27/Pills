# Immutable Skill Version Pinning

We evaluated allowing agents to bind to live, mutable skill drafts versus requiring immutable semantic release snapshots. We decided that Skill Studio produces immutable, semver-pinned Skill Releases, and Pills are bound to specific released versions. Modifying a skill creates a new draft version without altering production agents until an explicit admin promotion and evaluation phase (via Promptfoo) is performed. This prevents accidental regressions in live agent workflows and guarantees reproducible prompt engineering benchmarks.
