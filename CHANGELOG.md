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

Entity source names, IDs, register addresses, scales and control types are
preserved. ESPHome 2026.9 normalizes the slash in `Turn off/on status`; check its
Home Assistant entity when upgrading. Hardware verification is still pending.
