import sys, yaml
from rich import print as rprint
from .safety import Safety, SafetyConfig
from .via import VIA
from .adapters.elm327 import ELM327
try:
    from .adapters.socketcan import SocketCAN
except Exception:
    SocketCAN = None
from .skills import telemetry as sk_telemetry
from .skills import diagnostics as sk_diag

USAGE = """
Commands:
  telemetry      Show speed/RPM/coolant/SoC (read-only)
  diagnostics    Read DTCs (no clearing in S0)

Config file: config.vehicle.yaml
"""

def load_cfg(path="config.vehicle.yaml"):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def make_adapter(cfg):
    adapter = cfg.get("adapter","elm327")
    if adapter == "elm327":
        return ELM327(port=cfg.get("port","COM3"), baud=int(cfg.get("baud",115200)))
    elif adapter == "socketcan":
        if SocketCAN is None:
            raise RuntimeError("SocketCAN not available. pip install python-can")
        return SocketCAN(channel=cfg.get("channel","can0"))
    else:
        raise RuntimeError(f"Unknown adapter: {adapter}")

def run():
    if len(sys.argv) < 2 or sys.argv[1] in {"-h","--help","help"}:
        print(USAGE); return
    cfg = load_cfg()
    safety = Safety(SafetyConfig(mode=str(cfg.get("mode","S0"))))
    safety.ensure_read_only()

    a = make_adapter(cfg)
    via = VIA(a, profile=cfg.get("profile"))
    try:
        cmd = sys.argv[1]
        if cmd == "telemetry":
            sk_telemetry.run(via)
        elif cmd == "diagnostics":
            sk_diag.run(via)
        else:
            rprint(f"[red]Unknown command:[/red] {cmd}\n"+USAGE)
    finally:
        a.close()
