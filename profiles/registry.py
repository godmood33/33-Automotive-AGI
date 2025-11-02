import yaml, importlib.resources as rsrc
from typing import Dict, Any

class Profiles:
    def __init__(self):
        self.cache: Dict[str, Dict[str, Any]] = {}
    def load(self, name: str) -> Dict[str, Any]:
        if name in self.cache: return self.cache[name]
        for pkg in ("auto33.profiles.oem", "auto33.profiles.race"):
            try:
                with rsrc.files(pkg).joinpath(name+".yaml").open("r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                    self.cache[name] = data; return data
            except FileNotFoundError:
                continue
        raise FileNotFoundError(f"Profile '{name}' not found")
