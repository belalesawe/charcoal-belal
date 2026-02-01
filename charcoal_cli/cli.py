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
from charcoal_cli.commands.log import log

# Import subcommands
from charcoal_cli.commands.upstack_commands.onto import onto
from charcoal_cli.commands.upstack_commands.test import test as upstack_test
from charcoal_cli.commands.downstack_commands.get import get
from charcoal_cli.commands.downstack_commands.test import test as downstack_test
from charcoal_cli.commands.downstack_commands.track import track
from charcoal_cli.commands.stack_commands.test import test as stack_test
from charcoal_cli.commands.log_commands.default import default as log_default
from charcoal_cli.commands.log_commands.short import short as log_short
from charcoal_cli.commands.log_commands.long import long as log_long

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

# Register log subcommands
log.add_command(log_default)
log.add_command(log_short)
log.add_command(log_short, name="s")  # Alias for short
log.add_command(log_long)
log.add_command(log_long, name="l")  # Alias for long

# Register command groups with main CLI
main.add_command(log)
main.add_command(log, name="l")  # Alias for log
main.add_command(upstack)
main.add_command(upstack, name="us")  # Alias for upstack
main.add_command(downstack)
main.add_command(downstack, name="ds")  # Alias for downstack
main.add_command(stack)
main.add_command(stack, name="s")  # Alias for stack
