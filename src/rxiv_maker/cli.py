"""Command-line interface for rxiv-maker."""

import click
from rich.console import Console
from .__version__ import __version__

console = Console()


@click.command()
@click.version_option(version=__version__, prog_name="rxiv-maker")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
def main(verbose: bool) -> None:
    """Rxiv-Maker: Automated LaTeX article generation with modern CLI."""
    console.print(f"[bold green]Rxiv-Maker v{__version__}[/bold green]")
    console.print("Automated LaTeX article generation tool")
    
    if verbose:
        console.print("[dim]Verbose mode enabled[/dim]")
    
    console.print("\n[yellow]This is a placeholder implementation.[/yellow]")
    console.print("Core functionality will be implemented in future versions.")


if __name__ == "__main__":
    main()