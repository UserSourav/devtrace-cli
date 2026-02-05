import typer
import re
import tomllib
from pathlib import Path
from rich.console import Console

app = typer.Typer(help="Validate commits against rules")

console = Console(no_color=True)

@app.command()
def commit(
    msg_file: Path = typer.Argument(..., help="Commit message file"),
    rules_path: Path = typer.Option(Path(".devtrace\\configs\\rules.toml"), help="Rules file")
):
    if not msg_file.exists():
        print(f"Error: Message file not found: {msg_file}")
        raise typer.Exit(1)
    
    if not rules_path.exists():
        print(f"Error: Rules file not found: {rules_path}")
        raise typer.Exit(1)
    
    commit_msg = msg_file.read_text().strip().splitlines()[0]
    
    with rules_path.open('rb') as f:
        rules = tomllib.load(f)
    
    
    commit_pattern = rules.get('commit', {}).get('pattern')
    if commit_pattern and not re.match(commit_pattern, commit_msg):
        print("Invalid commit format! Expected: TICKET | TYPE : description")
        print(f"Got: {commit_msg}")
        raise typer.Exit(1)
    
    match = re.match(r'^([A-Z]+-\d+)\s\|\s([A-Z]+)\s:\s(.+)$', commit_msg)
    if not match:
        print("Could not parse commit: missing ticket/type/desc")
        raise typer.Exit(1)
    
    ticket, commit_type, desc = match.groups()
    
    ticket_pattern = rules.get('ticket', {}).get('pattern')
    if ticket_pattern and not re.match(ticket_pattern, ticket):
        print(f"Invalid ticket format: {ticket}")
        raise typer.Exit(1)
    
    if rules.get('ticket', {}).get('uppercase', False) and ticket != ticket.upper():
        print(f"Ticket must be uppercase: {ticket}")
        raise typer.Exit(1)
    
    allowed_types = rules.get('types', {}).get('allowed', [])
    if commit_type not in allowed_types:
        print(f"Unknown type: {commit_type} (allowed: {', '.join(allowed_types)})")
        raise typer.Exit(1)
    