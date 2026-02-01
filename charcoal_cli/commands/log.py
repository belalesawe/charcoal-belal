"""Log command group.

Commands that log your stacks.
Run `gt log --help` to learn more about visualization options.
"""

import click


@click.group(name="log", invoke_without_command=True)
@click.option(
    "-r",
    "--reverse",
    is_flag=True,
    default=False,
    help="Print the log upside down. Handy when you have a lot of branches!",
)
@click.option(
    "-s",
    "--stack",
    is_flag=True,
    default=False,
    help="Only show ancestors and descendants of the current branch.",
)
@click.option(
    "-n",
    "--steps",
    type=int,
    default=None,
    help="Only show this many levels upstack and downstack. Implies --stack.",
)
@click.option(
    "-u",
    "--show-untracked",
    is_flag=True,
    default=False,
    help="Include untracked branches in interactive selection.",
)
@click.pass_context
def log(
    ctx: click.Context,
    reverse: bool,
    stack: bool,
    steps: int | None,
    show_untracked: bool,
) -> None:
    """Commands that log your stacks.

    Run `gt log --help` to learn more about visualization options.
    """
    # If a subcommand is being invoked, don't run default behavior
    if ctx.invoked_subcommand is not None:
        return

    # Run default log action
    from charcoal_cli.actions.log import log_action
    from charcoal_cli.lib.context import create_context

    context = create_context()

    # Determine which branch to start from
    if steps or stack:
        branch_name = context.engine.current_branch_precondition
    else:
        branch_name = context.engine.trunk

    log_action(
        {
            "style": "FULL",
            "reverse": reverse,
            "branchName": branch_name,
            "steps": steps,
            "showUntracked": show_untracked,
        },
        context,
    )
