from typing import Any, Dict, List, Optional

class VehicleAdapter:
    name: str = "base"
    def connect(self, **kw):
        raise NotImplementedError
    def read_pid(self, pid: str) -> Optional[float]:
        return None
    def dtcs(self) -> List[str]:
        return []
    def close(self):
        pass
