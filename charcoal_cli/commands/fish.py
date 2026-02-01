"""Fish shell completion command."""

import click
from pathlib import Path


@click.command()
def fish() -> None:
    """Set up fish tab completion.

    Outputs the Fish shell completion script for the charcoal CLI.

    Installation:
        charcoal fish >> ~/.config/fish/completions/gt.fish

    After installation, restart your Fish shell or run:
        source ~/.config/fish/completions/gt.fish
    """
    # Read the gt.fish file from the lib directory
    fish_completion_file = Path(__file__).parent.parent / 'lib' / 'gt.fish'

    try:
        with open(fish_completion_file, 'r', encoding='utf-8') as f:
            content = f.read()
        click.echo(content)
    except FileNotFoundError:
        click.echo('Error: Fish completion file not found.', err=True)
        raise SystemExit(1)
