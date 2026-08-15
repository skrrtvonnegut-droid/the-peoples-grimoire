# Schemas

This directory is the canonical public home of The People's Grimoire JSON Schemas.

| Schema | Purpose |
| --- | --- |
| `grimoire-event.schema.json` | Normalized observation from an external system |
| `grimoire-connector.schema.json` | Connector capabilities, permissions, effects, and safety behavior |
| `grimoire-instance.schema.json` | Private deployment policy and connector bindings |
| `grimoire-artifact.schema.json` | Stable logical artifact identity, representations, and authority by concern |

The copies under `src/peoples_grimoire/schemas/` are distribution mirrors included in the Python package. CI requires them to remain byte-for-byte identical to these canonical files.

Schema versions are independent from the Python package version. A breaking schema change requires a new schema version, migration notes, and an ADR when it changes a trust boundary or core semantic.
