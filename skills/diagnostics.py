from rich.console import Console
from ..via import VIA

console = Console()

def run(via: VIA):
    dtcs = via.a.dtcs()
    if not dtcs:
        console.print("[green]No DTCs reported (or adapter doesn't support mode 03).[/green]")
    else:
        console.print("[yellow]DTCs:[/yellow]")
        for d in dtcs:
            console.print(f" - {d}")
