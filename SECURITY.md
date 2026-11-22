# Security Policy

## Scope

The project includes skill instructions and an optional Python-standard-library release-check/update helper. It has no project-operated server, authentication, telemetry or manuscript-upload connector. The helper defaults to read-only checks against the pinned official repository. Installation requires explicit consent, a supported unmodified standalone folder, official asset identity and checksum validation, safe archive paths, complete file inventories and a verified staged replacement. Managed/plugin/source-checkout installations require their owner or host's update process.

Checksums protect against corruption or mismatch, not compromise of the publisher or hosting account; they are not independent signatures. Future releases install instructions and scripts as data without executing downloaded code during installation. A verified old-version ZIP is retained by default; an installation can explicitly opt out. In either mode the original remains available during the swap, and a failed rollback reports its recovery path. Local concurrent/malicious filesystem changes are outside a complete security guarantee. See [update boundaries](skills/evidence-first-medical-writing/references/updates.md). Report archive handling, update rollback, unsafe instructions, privacy exposure, or packaging concerns through the private channel below.

## Reporting

Send private reports to `duyinapoleon@gmail.com` with:

- the affected file and version;
- a concise description and reproducible example;
- the potential impact;
- whether the report contains sensitive information.

Do not include patient identifiers, credentials, confidential manuscripts, or unnecessary personal data. Please allow a reasonable period for review before public disclosure.

For copyright, attribution, identity, privacy, or other rights concerns, use the same private contact and identify the exact repository path and requested remedy.
