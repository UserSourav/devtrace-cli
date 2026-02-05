import typer
from rich.console import Console
from importlib.metadata import version as version_lib

console = Console()

def version():
    """Show version"""
    pkg_version = version_lib("devtrace")
    console.print(f"devtrace version {pkg_version}")