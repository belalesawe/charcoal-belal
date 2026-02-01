"""Main CLI application entry point."""

import click


@click.group()
@click.option("--debug", is_flag=True, help="Enable debug output")
@click.option("--quiet", is_flag=True, help="Suppress non-error output")
@click.pass_context
def main(ctx: click.Context, debug: bool, quiet: bool) -> None:
    """charcoal CLI for managing stacked branches and related workflows."""
    ctx.ensure_object(dict)
    ctx.obj["debug"] = debug
    ctx.obj["quiet"] = quiet


# Import command groups
from charcoal_cli.commands.upstack import upstack
from charcoal_cli.commands.downstack import downstack
from charcoal_cli.commands.stack import stack

# Import subcommands
from charcoal_cli.commands.upstack_commands.onto import onto
from charcoal_cli.commands.upstack_commands.test import test as upstack_test
from charcoal_cli.commands.downstack_commands.get import get
from charcoal_cli.commands.downstack_commands.test import test as downstack_test
from charcoal_cli.commands.downstack_commands.track import track
from charcoal_cli.commands.stack_commands.test import test as stack_test

# Register subcommands to their groups
upstack.add_command(onto)
upstack.add_command(onto, name="o")  # Alias for onto
upstack.add_command(upstack_test)
upstack.add_command(upstack_test, name="t")  # Alias for test
downstack.add_command(get)
downstack.add_command(get, name="g")  # Alias for get
downstack.add_command(downstack_test)
downstack.add_command(downstack_test, name="t")  # Alias for test
downstack.add_command(track)
downstack.add_command(track, name="tr")  # Alias for track
stack.add_command(stack_test)
stack.add_command(stack_test, name="t")  # Alias for test

# Register command groups with main CLI
main.add_command(upstack)
main.add_command(upstack, name="us")  # Alias for upstack
main.add_command(downstack)
main.add_command(downstack, name="ds")  # Alias for downstack
main.add_command(stack)
main.add_command(stack, name="s")  # Alias for stack
