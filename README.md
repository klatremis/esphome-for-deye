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

### Known ESPHome 2026.9 warnings

- `skip_updates` no longer changes polling frequency. Sensors that previously
  requested slower polling now use the controller interval (15 seconds here).
  Check bus behavior on hardware before deploying this version widely. A polling
  redesign is tracked separately rather than silently changing register grouping.
- The existing `Turn off/on status` name contains `/`. ESPHome currently replaces
  this character with a Unicode fraction slash and warns; verify the entity in
  Home Assistant when upgrading. The source name is retained for this first update.

## Installation

1. Create an ESP32 device in ESPHome Device Builder and back up its YAML.
2. Copy [the configuration](<esphome config 10-8-2023.yaml>) into the device's YAML.
   The historical filename is retained for existing links.
3. Set `name` to your device name and adjust `device_type`, which prefixes entity
   names. Keep your existing values when upgrading an installed device.
4. Select the correct ESP32 board and UART pins. The example uses `esp32dev`,
   Arduino, TX GPIO17 and RX GPIO16, at 9600 baud.
5. Add your credentials to ESPHome's `secrets.yaml`:

   ```yaml
   wifi_ssid: "YOUR_WIFI_NAME"
   wifi_password: "YOUR_WIFI_PASSWORD"
   ```

6. Keep device-specific API encryption and OTA authentication settings from your
   existing configuration. Current ESPHome uses:

   ```yaml
   ota:
     - platform: esphome
       # password: !secret ota_password
   ```

7. Validate and compile in Device Builder. Install by USB for a new device;
   subsequent installations can use OTA when network access is working.
8. Add the device through the ESPHome integration in Home Assistant. Compare
   readings with the inverter display before using the controls.

For existing installations, preserve device and entity names, custom pins,
credentials and local changes. This maintenance update retains register
addresses, scales, entity names, and number/select types. It does not require
deleting the Home Assistant integration.

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

The [Time of Use card](<time of use card>) uses the HACS `multiple-entity-row`
custom card. Adapt the example entity IDs to your installation.

## Development and automated checks

Use Python 3.12 and install `requirements-dev.txt`, preferably in a virtual
environment. From the repository root:

```sh
python -m pip install -r requirements-dev.txt
# Copy tests/secrets.example.yaml to secrets.yaml for an offline build test.
esphome config "esphome config 10-8-2023.yaml"
esphome compile "esphome config 10-8-2023.yaml"
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

See [maintenance notes](docs/maintenance.md) for follow-up work.
