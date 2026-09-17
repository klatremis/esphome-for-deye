# Contributing

Make changes on a branch and open a pull request against `main`. Describe the
problem, resulting behavior, validation, and any Home Assistant migration needed.
Keep hardware-specific changes separate from shared register corrections.

## Source files

- `deye.yaml`: generic ESP32 hardware, connectivity and substitution defaults.
- `packages/deye.yaml`: Deye controller and shared register definitions.
- `dashboards/time-of-use.yaml`: Home Assistant card example.
- `docs/reference/`: original register reference; check applicability to the model.
- `esphome config 10-8-2023.yaml`: generated standalone compatibility copy.
  Edit the source files above, then run `python scripts/sync_legacy.py`.

## Checks

Use two-space YAML indentation, decimal register addresses and hexadecimal
bitmasks. Within entities, keep identification first, register decoding next,
then units/metadata, limits and filters or lambdas. Keep filter order unchanged:
for example, temperature offset must be applied before scaling. Preserve legacy
names and IDs even when their spelling is inconsistent; renaming needs a separate
migration. Prefer explicit ESPHome fields over YAML anchors for register entries.

Use Python 3.12 and install `requirements-dev.txt`. For development, copy
`tests/secrets.example.yaml` to `secrets.yaml` only if no real secrets file exists.
Never commit real credentials or upload firmware containing test credentials.

```sh
python scripts/sync_legacy.py --check
python tests/check_packages.py
esphome compile deye.yaml
git diff --check
```

CI runs configuration validation, package/standalone equivalence, local override
checks, and a firmware build. Dependabot proposes weekly ESPHome and Actions
dependency updates after its configuration reaches `main`; updates are reviewed
as pull requests and are not automatically merged.

A successful build is not a hardware test. Register corrections need an exact
inverter model, firmware version, documentation or raw-reading evidence, and a
comparison with the inverter display. Check charging and discharging for signed
values. Do not change entity names or domains without documenting migration.

## Releases

Merge only after CI passes and relevant hardware checks are recorded. Create a
version tag and GitHub release for a tested revision, with changes and supported
model/firmware evidence. Users can pin remote packages to that tag or a commit.
Never label build-only results as hardware-tested firmware. This update does not
publish a release or redistribute firmware built with dummy credentials.
