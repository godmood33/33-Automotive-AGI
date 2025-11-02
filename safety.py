from dataclasses import dataclass

@dataclass
class SafetyConfig:
    mode: str = "S0"  # S0 observe-only

class Safety:
    def __init__(self, cfg: SafetyConfig):
        self.cfg = cfg

    def ensure_read_only(self):
        # Placeholder for future gating
        return True

    def forbid_write(self, action: str):
        if self.cfg.mode == "S0":
            raise PermissionError(f"Blocked: '{action}' not allowed in S0 (read-only)")
