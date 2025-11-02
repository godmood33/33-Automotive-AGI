from rich.table import Table
from rich.console import Console
from ..via import VIA

console = Console()

def run(via: VIA):
    t = via.snapshot_basic()
    table = Table(title="Telemetry (S0)")
    table.add_column("Signal"); table.add_column("Value")
    table.add_row("speed_kph", str(t.speed_kph))
    table.add_row("rpm", str(t.rpm))
    table.add_row("coolant_c", str(t.coolant_c))
    table.add_row("soc_pct", str(t.soc_pct))
    console.print(table)
