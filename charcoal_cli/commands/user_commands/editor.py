"""User editor configuration command.

This command allows users to configure the default editor for Charcoal operations.
"""

import click

from charcoal_cli.lib.context import create_context


@click.command(name="editor")
@click.option(
    "--set",
    "set_value",
    type=str,
    default=None,
    help="Set default editor for Charcoal. eg --set vim.",
)
@click.option(
    "--unset",
    is_flag=True,
    default=False,
    help="Unset default editor for Charcoal.",
)
@click.pass_context
def editor(ctx: click.Context, set_value: str | None, unset: bool) -> None:
    """The editor opened by Charcoal.

    Query the current editor, set a new editor, or unset to use git default.
    """
    context = create_context()

    if set_value:
        # Set the editor
        context.userConfig.update(lambda data: setattr(data, "editor", set_value))
        context.splog.info(f"Editor set to {set_value}")
    elif unset:
        # Unset the editor
        context.userConfig.update(lambda data: setattr(data, "editor", None))
        git_editor = context.userConfig.data.get_editor()
        context.splog.info(
            f"Editor preference erased. Defaulting to your git editor (currently {git_editor})"
        )
    else:
        # Query mode
        if context.userConfig.data.editor:
            context.splog.info(context.userConfig.data.editor)
        else:
            git_editor = context.userConfig.data.get_editor()
            context.splog.info(
                f"Editor is not set. Charcoal will use your git editor (currently {git_editor})"
            )
