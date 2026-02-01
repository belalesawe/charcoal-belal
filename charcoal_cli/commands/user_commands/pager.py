"""User pager configuration command.

This command allows users to configure the default pager for Charcoal output.
"""

import click

from charcoal_cli.lib.context import create_context


@click.command(name="pager")
@click.option(
    "--set",
    "set_value",
    type=str,
    default=None,
    help='Set default pager for Charcoal. e.g. --set "less -FRX".',
)
@click.option(
    "--disable",
    is_flag=True,
    default=False,
    help="Disable pager for Charcoal",
)
@click.option(
    "--unset",
    is_flag=True,
    default=False,
    help="Unset default pager for Charcoal and default to git pager.",
)
@click.pass_context
def pager(ctx: click.Context, set_value: str | None, disable: bool, unset: bool) -> None:
    """The pager opened by Charcoal.

    Query the current pager, set a new pager, disable it, or unset to use git default.
    """
    context = create_context()

    if disable:
        # Disable pager by setting it to empty string
        context.userConfig.update(lambda data: setattr(data, "pager", ""))
        context.splog.info("Pager disabled")
    elif set_value:
        # Set the pager
        context.userConfig.update(lambda data: setattr(data, "pager", set_value))
        context.splog.info(f"Pager set to {set_value}")
    elif unset:
        # Unset the pager
        context.userConfig.update(lambda data: setattr(data, "pager", None))
        current_pager = context.userConfig.data.get_pager()
        if current_pager:
            context.splog.info(
                f"Pager preference erased. Defaulting to your git pager (currently {current_pager})"
            )
        else:
            context.splog.info(
                "Pager preference erased. Defaulting to your git pager (currently disabled)"
            )
    else:
        # Query mode
        current_pager = context.userConfig.data.get_pager()
        if not current_pager:
            context.splog.info("Pager is disabled")
        elif context.userConfig.data.pager:
            context.splog.info(context.userConfig.data.pager)
        else:
            context.splog.info(
                f"Pager is not set. Charcoal will use your git pager (currently {current_pager})"
            )
