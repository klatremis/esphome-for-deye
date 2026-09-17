# Changelog

## Unreleased

- Set default Modbus polling to 20 seconds; expose interval, address and UART pins
  through substitutions.
- Separate the generic device configuration from shared Deye registers.
- Preserve the historical standalone YAML as a generated compatibility copy.
- Move the dashboard example and register reference into dedicated directories.
- Enable the ESPHome OTA platform explicitly.
- Add ESPHome 2026.9.0 validation, compilation and package checks in GitHub Actions.
- Add Dependabot update proposals and contribution/release guidance.
- Remove ignored `skip_updates` fields. All registers now follow the configured
  controller interval; this changes polling compared with older ESPHome versions.

- Standardize YAML indentation, field order, bitmask notation and section comments.
- Remove unreachable code from the running-state decoder.
- Connect `device_description` to ESPHome's device comment.
- Write `Turn off⁄on status` explicitly, matching ESPHome 2026.9's existing
  normalization and removing the slash deprecation warning.

Resolved entity names on ESPHome 2026.9, IDs, register addresses, scales and control
types are preserved. Check the status entity when upgrading from older ESPHome.
Hardware verification is still pending.
