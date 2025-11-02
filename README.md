# 33 Automotive AGI

Universal, modular **Automotive AGI** core for road and race vehicles — built safety‑first.

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-S0--read--only-orange.svg)

## Features
- **S0 Read-only:** no writes or actuation by default
- **Buses/Protocols:** OBD‑II (J1979), UDS (ISO‑14229), DoIP (ISO‑13400) [planned], CAN/CAN‑FD, SocketCAN (Linux)
- **Adapters:** ELM327/OBDLink (Windows serial), SocketCAN (Linux/RPi)
- **Profiles:** YAML signal maps per OEM / series (examples included)
- **Skills:** Telemetry & Diagnostics (read DTCs)

## Quick Start

### 1) Create a venv & install
```bash
python -m venv .venv
# Windows
# . .\.venv\Scripts\Activate.ps1
# Linux/Mac
# source .venv/bin/activate

pip install -U pip
pip install -e .
```

### 2) Configure
Create `config.vehicle.yaml` in the repo root:

```yaml
adapter: elm327        # elm327 | socketcan
port: COM7             # Windows example; omit for socketcan
baud: 115200
mode: S0               # observe-only
profile: vag           # optional: loads profiles/oem/vag.yaml
```

### 3) Run
```bash
python -m auto33.main telemetry
python -m auto33.main diagnostics
```

## Safety
- Default mode **S0** blocks any write/service/actuation.
- No seed‑key bypasses, no proprietary decryption.
- Logs and data remain local by default.

## License
MIT © Ibrahim (godmood33)
