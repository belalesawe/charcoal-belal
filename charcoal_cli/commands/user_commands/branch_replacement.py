"""Branch replacement character configuration command for Charcoal CLI."""

import click

from charcoal_cli.lib.context import create_context


@click.command(name="branch-replacement")
@click.option(
    "--set-underscore",
    is_flag=True,
    default=False,
    help="Use underscore (_) as the replacement character",
)
@click.option(
    "--set-dash",
    is_flag=True,
    default=False,
    help="Use dash (-) as the replacement character",
)
@click.option(
    "--set-empty",
    is_flag=True,
    default=False,
    help="Remove invalid characters from the branch name without replacing them",
)
def branch_replacement(set_underscore: bool, set_dash: bool, set_empty: bool) -> None:
    """The character that will replace unsupported characters in generated branch names."""
    context = create_context()

    if set_underscore:
        context.userConfig.update(lambda data: setattr(data, "branchReplacement", "_"))
        context.splog.info("Set underscore (_) as the replacement character")
    elif set_dash:
        context.userConfig.update(lambda data: setattr(data, "branchReplacement", "-"))
        context.splog.info("Set dash (-) as the replacement character")
    elif set_empty:
        context.userConfig.update(lambda data: setattr(data, "branchReplacement", ""))
        context.splog.info("Invalid characters will be removed without being replaced")
    else:
        # Query mode
        replacement = context.userConfig.data.branchReplacement
        if replacement == "":
            context.splog.info("Invalid characters will be removed without being replaced")
        elif replacement:
            context.splog.info(f"Invalid characters will be replaced with {replacement}")
        else:
            # Default behavior (assuming dash is default)
            context.splog.info("Invalid characters will be replaced with -")
