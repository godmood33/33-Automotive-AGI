# Windows/serial ELM327/OBDLink (STN preferred). Read-only PIDs.
import time
from typing import Optional
try:
    import serial  # type: ignore
except Exception as e:
    serial = None
from .base import VehicleAdapter

def _rpm(a: int, b: int) -> float:
    return ((a*256)+b)/4.0
def _speed(a: int) -> float:
    return float(a)
def _coolant(a: int) -> float:
    return float(a-40)

DECODERS = {"010C": _rpm, "010D": _speed, "0105": _coolant}

class ELM327(VehicleAdapter):
    name = "elm327"
    def __init__(self, port: str, baud: int = 115200, timeout: float = 1.0):
        if serial is None:
            raise RuntimeError("pyserial not installed. pip install pyserial")
        self.s = serial.Serial(port, baudrate=baud, timeout=timeout)
        self._init()
    def _w(self, cmd: str) -> bytes:
        self.s.write((cmd+"\r").encode()); return self.s.read_until(b">")
    def _init(self):
        for c in ["ATZ","ATE0","ATL0","ATS0","ATH0","ATSP0"]:
            try:
                self._w(c)
                time.sleep(0.05)
            except Exception:
                pass
    def read_pid(self, pid: str) -> Optional[float]:
        if not pid.startswith("01"):
            return None
        try:
            out = self._w(f"01{pid[2:]}").decode(errors="ignore")
            toks = [t for t in out.replace("\r"," ").split() if all(c in "0123456789ABCDEF" for c in t)]
            data = [int(x,16) for x in toks[-2:]]
            fn = DECODERS.get(pid)
            if fn is None:
                return None
            return fn(*data)
        except Exception:
            return None
    def dtcs(self):
        try:
            out = self._w("03").decode(errors="ignore")
            return [out.strip()] if out else []
        except Exception:
            return []
    def close(self):
        try: self.s.close()
        except Exception: pass
