# Maintenance scope and follow-up

## First compatibility update

- Pin development/build checks to ESPHome 2026.9.0.
- Migrate the legacy empty `ota:` entry to the ESPHome OTA platform.
- Validate and compile the generic ESP32/Arduino example in CI.
- Preserve resolved entity names, IDs, registers, scaling, and control types.
- Standardize YAML formatting, field order, bitmasks and section comments.
- Remove an unreachable return from the running-state decoder and expose the
  existing device description as ESPHome metadata.
- Write the already-normalized status name explicitly to eliminate the slash warning.
- Keep the historical standalone filename as an automatically generated copy.
- Separate generic hardware/connectivity from the shared register package.
- Use configurable 20-second polling and remove ignored `skip_updates` fields.
- Add package equivalence/override tests and Dependabot update proposals.

Hardware testing of this update is pending. A successful compiler run verifies
the firmware build, not inverter compatibility or register semantics.

## Existing contributions reviewed

- [PR #23](https://github.com/klatremis/esphome-for-deye/pull/23): changes Time of
  Use starts from numbers to selects. This changes the Home Assistant entity
  domain and needs a migration plan. The diff targets an old filename and some
  slots omit 23:30. Review separately.
- [PR #27](https://github.com/klatremis/esphome-for-deye/pull/27): adds termination
  guidance. The README now asks users to check termination and existing resistors
  without prescribing the same arrangement for every bus.
- [PR #39](https://github.com/klatremis/esphome-for-deye/pull/39): writes preset
  complete values to register 178. These combine several settings; review bit
  definitions and preservation of unrelated settings before incorporating it.

No existing PR has been merged or closed as part of this review.

## Next investigations

- ESPHome 2026.9.0 warns that `skip_updates` has no effect and will be removed in
  2027.3.0. The ignored fields have been removed and 20-second polling is now
  explicit. Review bus load on hardware before considering separate slower controllers.
- The status name uses an explicit Unicode fraction slash, matching ESPHome
  2026.9 normalization. Check entity identity when upgrading older installations.

- [Issue #45](https://github.com/klatremis/esphome-for-deye/issues/45): investigate
  total imported/exported energy rollover. The current configuration uses one
  word at 522 and 524; compare with the model's documented two-word counters
  before changing decoding and affecting historical statistics.
- [Issue #26](https://github.com/klatremis/esphome-for-deye/issues/26): the report
  lacks the failing configuration/log context. A build of the checked-in file
  helps distinguish repository errors from local YAML/lambda edits.
- Track all three low-voltage families listed in the README, with exact model
  and firmware evidence. The maintainer's 20K configuration is a separate
  reference, not proof that every model is tested.
- Validate battery channel 2 register 594, signed decoding and scaling on the
  SG05 14–20K family before adding it to a model-specific profile.
