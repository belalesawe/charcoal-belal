"""User tips configuration command.

This command allows users to enable or disable usage tips in the CLI.
"""

import click

from charcoal_cli.lib.context import create_context


@click.command(name="tips")
@click.option(
    "--enable",
    is_flag=True,
    default=False,
    help="Enable tips.",
)
@click.option(
    "--disable",
    is_flag=True,
    default=False,
    help="Disable tips.",
)
@click.pass_context
def tips(ctx: click.Context, enable: bool, disable: bool) -> None:
    """Show tips while using Charcoal.

    Query, enable, or disable usage tips.
    """
    context = create_context()

    if enable:
        context.userConfig.update(lambda data: setattr(data, "tips", True))
        context.splog.info("tips enabled")
    elif disable:
        context.userConfig.update(lambda data: setattr(data, "tips", False))
        context.splog.info("tips disabled")
    else:
        # Query mode
        if context.userConfig.data.tips:
            context.splog.info("tips enabled")
        else:
            context.splog.info("tips disabled")
