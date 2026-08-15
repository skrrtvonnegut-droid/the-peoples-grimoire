# Synthetic Trust Manifests

These files describe a fictional, read-only Notion and GitHub deployment. They contain no live account, workspace, repository, page, person, or credential data.

```bash
grimoire validate examples/manifests
```

The bundle demonstrates four boundaries:

1. Connector capability manifests declare effects and minimum permissions before an instance enables them.
2. Instance configuration stores credential **references**, never secret values.
3. Resource allowlists bound discovery to explicitly selected roots.
4. Artifact authority is assigned by semantic concern rather than treating two SaaS copies as co-equal truth.

The capability scope strings are illustrative contract vocabulary, not instructions for configuring production credentials. Provider-specific scope guidance must be verified against current official documentation when the real connectors are implemented.
