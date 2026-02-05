import typer
from rich.console import Console

console = Console()

def hello():
    """Say hello in style"""
    console.print(f"[bold green]Hello DevTrace[/]")