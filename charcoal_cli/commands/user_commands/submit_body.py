"""User submit-body configuration command.

This command configures whether to include commit messages in PR descriptions.
"""

import click

from charcoal_cli.lib.context import create_context


@click.command(name="submit-body")
@click.option(
    "--include-commit-messages/--no-include-commit-messages",
    default=None,
    help="Include commit messages in PR body by default.",
)
@click.pass_context
def submit_body(ctx: click.Context, include_commit_messages: bool | None) -> None:
    """Options for default PR descriptions.

    Query or configure whether to include commit messages in PR bodies.
    """
    context = create_context()

    if include_commit_messages is True:
        context.userConfig.update(
            lambda data: setattr(data, "submitIncludeCommitMessages", True)
        )
        context.splog.info("default PR body will include commit messages")
    elif include_commit_messages is False:
        context.userConfig.update(
            lambda data: setattr(data, "submitIncludeCommitMessages", False)
        )
        context.splog.info("default PR body will not include commit messages")
    else:
        # Query mode
        if context.userConfig.data.submitIncludeCommitMessages:
            context.splog.info("default PR body will include commit messages")
        else:
            context.splog.info("default PR body will not include commit messages")
