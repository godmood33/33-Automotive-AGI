from dataclasses import dataclass
from typing import Optional, Dict, Any
from .adapters.base import VehicleAdapter
from .profiles.registry import Profiles

@dataclass
class Telemetry:
    speed_kph: Optional[float] = None
    rpm: Optional[float] = None
    coolant_c: Optional[float] = None
    soc_pct: Optional[float] = None

class VIA:
    def __init__(self, adapter: VehicleAdapter, profile: Optional[str] = None):
        self.a = adapter
        self.prof = Profiles().load(profile) if profile else None

    def snapshot_basic(self) -> Telemetry:
        # fall back to standard OBD-II PIDs
        speed = self.get("speed_kph") if self.prof else self.a.read_pid("010D")
        rpm = self.get("rpm") if self.prof else self.a.read_pid("010C")
        coolant = self.get("coolant_c") if self.prof else self.a.read_pid("0105")
        soc = self.get("soc_pct") if self.prof else self.a.read_pid("soc")
        return Telemetry(speed_kph=speed, rpm=rpm, coolant_c=coolant, soc_pct=soc)

    def get(self, key: str) -> Optional[float]:
        if not self.prof:
            return None
        spec = self.prof.get("signals", {}).get(key)
        if not spec:
            return None
        t = spec.get("type")
        if t == "pid":
            return self.a.read_pid(spec["id"])
        # placeholders for uds/can mappings in future
        return None

    def snapshot_ext(self) -> Dict[str, Any]:
        keys = self.prof.get("signals", {}).keys() if self.prof else []
        return {k: self.get(k) for k in keys}
