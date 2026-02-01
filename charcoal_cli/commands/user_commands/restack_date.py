"""Restack date configuration command for Charcoal CLI."""

import click

from charcoal_cli.lib.context import create_context


@click.command(name="restack-date")
@click.option(
    "--use-author-date/--no-use-author-date",
    default=None,
    help=(
        "Passes `--committer-date-is-author-date` to the internal git rebase for restack operations. "
        "Instead of using the current time as the committer date, use the author date of the commit being rebased as the committer date. "
        "To return to default behavior, pass in `--no-use-author-date`"
    ),
)
def restack_date(use_author_date: bool | None) -> None:
    """Configure how committer date is handled by restack internal rebases."""
    context = create_context()

    if use_author_date is None:
        # Query mode
        if context.userConfig.data.restackCommitterDateIsAuthorDate:
            context.splog.info(
                "`--committer-date-is-author-date` will be passed to the internal `git rebase`"
            )
        else:
            context.splog.info(
                "`--committer-date-is-author-date` will not be passed to the internal `git rebase`"
            )
    elif use_author_date:
        context.userConfig.update(
            lambda data: setattr(data, "restackCommitterDateIsAuthorDate", True)
        )
        context.splog.info(
            "`--committer-date-is-author-date` will be passed to the internal `git rebase`"
        )
    else:
        context.userConfig.update(
            lambda data: setattr(data, "restackCommitterDateIsAuthorDate", False)
        )
        context.splog.info(
            "`--committer-date-is-author-date` will not be passed to the internal `git rebase`"
        )
