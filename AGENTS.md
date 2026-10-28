# Building services with Neton

Use the Neton development skill from the canonical neton-docs `skills/neton-development`
directory when available. Resolve this application's pinned Framework and KSP versions
before using examples: beta26 still uses `neton.ws`, while post-beta26 candidates use
`neton.websocket`. Do not upgrade imports without matching dependencies.

Use this public application as a minimal server foundation, not an admin product.
Follow Neton Config SPI, generated controller routes, injected services and owned
resource lifecycles. Add persistence with explicit migrations only when required.
AI-assisted development does not require the optional runtime `neton-ai` dependency.
Specs and skills live in https://github.com/netonframework/netonframework.github.io;
installing framework dependencies does not automatically install a skill.

Verify actual requested behavior and failure paths. For release readiness use the
existing acceptance scripts; do not substitute debug compilation for runtime evidence.
