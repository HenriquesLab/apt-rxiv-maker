"""Command-line interface for rxiv-maker."""

import click
from rich.console import Console
from .__version__ import __version__
from .version_check import validate_critical_dependencies, check_all_dependencies

console = Console()


@click.command()
@click.version_option(version=__version__, prog_name="rxiv-maker")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
@click.option("--check-deps", is_flag=True, help="Check dependency versions and compatibility")
def main(verbose: bool, check_deps: bool) -> None:
    """Rxiv-Maker: Automated LaTeX article generation with modern CLI."""
    
    # Validate critical dependencies first
    validate_critical_dependencies()
    
    console.print(f"[bold green]Rxiv-Maker v{__version__}[/bold green]")
    console.print("Automated LaTeX article generation tool")
    
    if verbose:
        console.print("[dim]Verbose mode enabled[/dim]")
    
    if check_deps:
        console.print("\n[cyan]Checking dependencies...[/cyan]")
        results = check_all_dependencies(warn_on_issues=False)
        
        for package, (is_compatible, installed_ver, required_ver) in results.items():
            status_icon = "✅" if is_compatible else ("❌" if installed_ver is None else "⚠️")
            status_color = "green" if is_compatible else ("red" if installed_ver is None else "yellow")
            installed_str = installed_ver or "not installed"
            console.print(f"  {status_icon} [{status_color}]{package:15}[/] {installed_str:15} (required: {required_ver})")
        
        compatible_count = sum(1 for is_compat, _, _ in results.values() if is_compat)
        total_count = len(results)
        console.print(f"\nCompatibility: [{('green' if compatible_count == total_count else 'yellow')}]{compatible_count}/{total_count}[/] packages meet requirements")
        return
    
    # Check dependencies silently and show warnings if needed
    check_all_dependencies(warn_on_issues=True)
    
    console.print("\n[yellow]This is a placeholder implementation.[/yellow]")
    console.print("Core functionality will be implemented in future versions.")
    console.print("\n[dim]Tip: Use --check-deps to verify dependency compatibility[/dim]")


if __name__ == "__main__":
    main()