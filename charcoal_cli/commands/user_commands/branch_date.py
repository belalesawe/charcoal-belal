"""User branch-date configuration command.

This command configures whether to prepend date to auto-generated branch names.
"""

import click

from charcoal_cli.lib.context import create_context


@click.command(name="branch-date")
@click.option(
    "--enable",
    is_flag=True,
    default=False,
    help="Enable date in auto-generated branch names",
)
@click.option(
    "--disable",
    is_flag=True,
    default=False,
    help="Disable date in auto-generated branch names",
)
@click.pass_context
def branch_date(ctx: click.Context, enable: bool, disable: bool) -> None:
    """Toggle prepending date to auto-generated branch names on branch creation.

    Query, enable, or disable date prepending.
    """
    context = create_context()

    if enable:
        context.userConfig.update(lambda data: setattr(data, "branchDate", True))
        context.splog.info("Enabled date")
    elif disable:
        context.userConfig.update(lambda data: setattr(data, "branchDate", False))
        context.splog.info("Disabled date")
    else:
        # Query mode
        branch_date_enabled = context.userConfig.data.branchDate
        if branch_date_enabled:
            context.splog.info("Branch date is enabled")
        else:
            context.splog.info("Branch date is disabled")
