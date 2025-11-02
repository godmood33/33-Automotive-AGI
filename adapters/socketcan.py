# Linux SocketCAN skeleton (read one frame opportunistically)
from typing import List
try:
    import can  # type: ignore
except Exception as e:
    can = None
from .base import VehicleAdapter

class SocketCAN(VehicleAdapter):
    name = "socketcan"
    def __init__(self, channel: str = "can0"):
        if can is None:
            raise RuntimeError("python-can not installed. pip install python-can")
        self.bus = can.interface.Bus(channel=channel, bustype="socketcan")
    def read_pid(self, pid: str):
        # Not applicable for raw CAN in MVP
        return None
    def dtcs(self) -> List[str]:
        return []
    def close(self):
        try: self.bus.shutdown()
        except Exception: pass
