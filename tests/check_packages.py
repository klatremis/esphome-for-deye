"""Integration checks for package expansion and user overrides (no hardware)."""

from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

import yaml

ROOT = Path(__file__).resolve().parents[1]


class ConfigLoader(yaml.SafeLoader):
    pass


# Preserve ESPHome scalar tags for comparison without executing their contents.
ConfigLoader.add_multi_constructor(
    "!", lambda loader, tag, node: (tag, loader.construct_scalar(node))
)


def validate(path):
    result = subprocess.run(
        [sys.executable, "-X", "utf8", "-m", "esphome", "config", str(path)],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
    )
    if result.returncode:
        raise RuntimeError(result.stderr + result.stdout)
    return yaml.load(result.stdout, Loader=ConfigLoader)


def main():
    package = validate(ROOT / "deye.yaml")
    legacy = validate(ROOT / "esphome config 10-8-2023.yaml")
    assert package == legacy, "Package and standalone configurations differ"
    assert package["modbus_controller"][0]["update_interval"] == "20s"

    with tempfile.TemporaryDirectory(prefix="deye-test-") as directory:
        test_dir = Path(directory)
        shutil.copy(ROOT / "tests/secrets.example.yaml", test_dir / "secrets.yaml")
        entry = test_dir / "custom.yaml"
        include_path = (ROOT / "deye.yaml").as_posix()
        entry.write_text(
            'substitutions:\n'
            '  name: deye-test\n'
            '  device_type: custom\n'
            '  modbus_controller_id: custom_controller\n'
            '  modbus_address: "2"\n'
            '  update_interval: 30s\n'
            '  tx_pin: "22"\n'
            '  rx_pin: "21"\n'
            f'packages:\n  deye: !include "{include_path}"\n',
            encoding="utf-8",
        )
        custom = validate(entry)
        assert custom["esphome"]["name"] == "deye-test"
        controller = custom["modbus_controller"][0]
        assert controller["id"] == "custom_controller"
        assert controller["address"] == 2
        assert controller["update_interval"] == "30s"
        assert custom["uart"][0]["tx_pin"]["number"] == 22
        assert custom["uart"][0]["rx_pin"]["number"] == 21
        for domain in ("sensor", "binary_sensor", "text_sensor", "switch", "number", "select"):
            for entity in custom[domain]:
                assert entity["name"].startswith("custom")
                assert entity["modbus_controller_id"] == "custom_controller"
    print("Package/standalone equivalence and local overrides verified.")


if __name__ == "__main__":
    main()
