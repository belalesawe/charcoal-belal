"""Branch prefix configuration command for Charcoal CLI."""

import click

from charcoal_cli.lib.context import create_context
from charcoal_cli.lib.utils.branch_name import set_branch_prefix


@click.command(name="branch-prefix")
@click.option(
    "-s",
    "--set",
    "set_value",
    type=str,
    default=None,
    help="Set a new prefix for branch names.",
)
@click.option(
    "-r",
    "--reset",
    is_flag=True,
    default=False,
    help="Turn off branch prefixing. Takes precedence over --set",
)
def branch_prefix(set_value: str | None, reset: bool) -> None:
    """The prefix which Charcoal will prepend to generated branch names."""
    context = create_context()

    if reset:
        context.userConfig.update(lambda data: setattr(data, "branchPrefix", None))
        context.splog.info("Reset branch-prefix")
    elif set_value:
        # Sanitize the prefix before storing it
        sanitized_prefix = set_branch_prefix(set_value, context)
        # Show the user what was actually stored (may differ from input if sanitized)
        context.splog.info(f'Set branch-prefix to "{sanitized_prefix}"')
    else:
        # Query mode
        prefix = context.userConfig.data.branchPrefix
        if prefix:
            context.splog.info(prefix)
        else:
            context.splog.info(
                "branch-prefix is not set. Try running `charcoal user branch-prefix --set <prefix>` to update the value."
            )
