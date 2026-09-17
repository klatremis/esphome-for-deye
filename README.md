# ESPHome for Deye

ESPHome configuration for local monitoring and control of Deye three-phase,
low-voltage hybrid inverters in Home Assistant over RS485/Modbus.
Choose an ESP32 and RS485 adapter suitable for your installation.

## Inverter compatibility

| Model family | Status |
| --- | --- |
| SUN-5/6/8/10/12K-SG04LP3-EU | Original target family; SUN-12K was confirmed on hardware in the original project. |
| SUN-3/4/5/6/8/10/12K-SG05LP3-EU-SM2 | Maintainer reports compatibility with the SG04 register map; individual models and firmware versions still need documented verification. |
| SUN-14/15/16/18/20K-SG05LP3-EU-SM2 | Maintainer runs a separate adapted configuration on a 20K model. This repository does not yet provide that profile or a second battery-current sensor. |

Single-phase and high-voltage models are outside this configuration's scope.
Do not choose a register map based on the Deye brand alone.

The development dependency is pinned to **ESPHome 2026.9.0**. GitHub Actions
validates and compiles the generic ESP32/Arduino configuration. A passing build
does not verify Modbus readings or control behavior on an inverter.

## Repository layout

| Path | Purpose |
| --- | --- |
| `deye.yaml` | Short generic ESP32 configuration and user-adjustable defaults |
| `packages/deye.yaml` | Shared Deye register definitions and controller |
| `dashboards/time-of-use.yaml` | Home Assistant card example |
| `docs/reference/deye-3phase-modbus.docx` | Original Modbus reference document |
| `esphome config 10-8-2023.yaml` | Generated standalone copy for existing links |
| `.github/workflows/esphome.yaml` | Automatic validation and firmware compilation |

## Installation using a GitHub package

Keep a small local YAML in ESPHome Device Builder. The shared configuration is
fetched from GitHub when ESPHome processes/builds it; repository changes do not
flash your device automatically. [ESPHome packages documentation](https://esphome.io/components/packages/).

```yaml
substitutions:
  name: deye12
  device_type: sun12k
  modbus_controller_id: sg04lp3
  modbus_address: "1"
  update_interval: 20s
  esp32_board: esp32dev
  tx_pin: "17"
  rx_pin: "16"

packages:
  deye: github://klatremis/esphome-for-deye/deye.yaml@main

wifi:
  ssid: !secret wifi_ssid
  password: !secret wifi_password
```

The package files must be present on the selected Git ref. While PR #55 is still
unmerged, use `@codex/esphome-maintenance` instead of `@main` for preview testing.
For a deployed installation, replace `@main` with a reviewed commit SHA or a
published release tag to keep builds reproducible. This update has no release tag
yet. Change the reference deliberately when upgrading.

1. Back up your current device YAML. Preserve existing `name`, `device_type` and
   `modbus_controller_id` values when migrating; the example defaults are not a
   reason to rename an installed device.
2. Select the board and UART pins appropriate for your ESP32/RS485 adapter. This
   example uses automatic direction control and Modbus address 1 at 9600 baud.
3. Store `wifi_ssid` and `wifi_password` in your local `secrets.yaml`.
4. Keep device-specific API encryption, OTA authentication, hardware startup
   actions, and other local customizations in your local YAML. Replace the old
   copied register definitions with the package; do not keep both sets of entities.
5. Validate and compile in Device Builder. Install by USB for a new device;
   subsequent installations can use OTA when network access is working.
6. Add the device through Home Assistant's ESPHome integration. Compare readings
   with the inverter display before using the controls.

The generic package includes Wi-Fi and an ESP32/Arduino setup. For other hardware
or networking arrangements, include only `packages/deye.yaml` and supply your own
hardware/connectivity configuration, a Modbus bus with ID `modbus1`, and the
`modbus_controller_id`, `modbus_address`, `device_type`, `update_interval`
substitutions. Hardware and inverter model are independent choices.

### Existing manual installations

The [historical standalone configuration](<esphome config 10-8-2023.yaml>) remains
available and is generated from the package sources. Existing copied configurations
continue to work independently; they do not automatically switch to packages.
For a local repository checkout, `deye.yaml` includes `packages/deye.yaml` directly.

This update preserves entity source names, IDs, register addresses, scales and
number/select types. Keep your credentials and customizations when upgrading.
Deleting the Home Assistant integration is not required.

### Polling and upgrade notes

The default is **20 seconds**, adjustable through `update_interval`. ESPHome
2026.9 ignores `skip_updates`, so those obsolete fields have been removed.
All register groups follow the controller interval. This differs from older
ESPHome behavior; check communication logs for timeouts and CRC errors on hardware.

The existing `Turn off/on status` name contains `/`. ESPHome 2026.9 normalizes it
to a Unicode fraction slash and warns that this becomes an error in 2027.7.0.
Verify the existing Home Assistant entity after upgrading; a deliberate name
migration is tracked separately.

## Hardware

- ESP32 with a suitable power supply.
- RS485 transceiver compatible with ESP32 logic levels. The example assumes
  automatic direction control; adapters requiring it need `flow_control_pin`
  configured under `modbus`.
- Wiring matched to the exact inverter model and port pinout.

![Original ESP32/RS485 wiring example](https://user-images.githubusercontent.com/22115157/211201233-f5fe9189-e6b3-4ee1-9baa-48068f078127.jpg)

The diagram is the original hardware example, not a universal pinout. Check UART
TX/RX, RS485 polarity, port selection, slave address (default `0x1`), and serial
settings if the inverter does not respond. Use termination appropriate for the
RS485 bus and account for resistors already fitted to the hardware.

The original installation used CN2 pins 7/8 and a 12 V to USB converter. Verify
the supply and pinout for your model. If the inverter also powers the ESP32,
turning the inverter off can remove remote access.

For the maintainer's LilyGO hardware, see [klatremis/hw](https://github.com/klatremis/hw).
Its GPIO setup differs from this generic example.

## Home Assistant dashboard

![Home Assistant example](https://user-images.githubusercontent.com/22115157/211201343-1d54cada-4b2c-40b0-88c4-faf31e17fead.png)

The [Time of Use card](dashboards/time-of-use.yaml) uses the HACS `multiple-entity-row`
custom card. Adapt the example entity IDs to your installation.

## Development and automated checks

Use Python 3.12 and install `requirements-dev.txt`, preferably in a virtual
environment. From the repository root:

```sh
python -m pip install -r requirements-dev.txt
# Copy tests/secrets.example.yaml to secrets.yaml for an offline build test.
python scripts/sync_legacy.py --check
python tests/check_packages.py
esphome compile deye.yaml
```

`tests/secrets.example.yaml` contains dummy Wi-Fi credentials. Do not overwrite
real credentials or flash firmware built with these dummy values. `secrets.yaml`,
virtual environments and build output are excluded from Git.

GitHub Actions runs these checks for pull requests and pushes to `main`, and can
also be started manually. CI never uploads firmware to a device. To update the
ESPHome baseline, change `requirements-dev.txt` and this README together, then
validate and compile before merging.

When reporting an issue, include the full inverter model, inverter firmware,
ESPHome version, ESP32/RS485 hardware, and relevant logs with secrets removed.
For incorrect readings, include the register and simultaneous inverter display
value where possible.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the branch, pull request and release workflow,
[CHANGELOG.md](CHANGELOG.md) for changes, and [maintenance notes](docs/maintenance.md)
for follow-up work. Dependabot proposes weekly dependency updates after merge;
updates are tested and reviewed rather than automatically merged.
