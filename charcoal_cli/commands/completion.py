"""Shell completion generation command."""

import click
import os


BASH_COMPLETION_SCRIPT = '''# Bash completion for charcoal/gt
# To install: charcoal completion >> ~/.bash_completion
# Or: charcoal completion >> ~/.bashrc

_charcoal_completion() {
    local IFS=$'\\n'
    local response

    response=$(env COMP_WORDS="${COMP_WORDS[*]}" COMP_CWORD=$COMP_CWORD _CHARCOAL_COMPLETE=bash_complete $1)

    for completion in $response; do
        IFS=',' read type value <<< "$completion"

        if [[ $type == 'dir' ]]; then
            COMPREPLY=()
            compopt -o dirnames
        elif [[ $type == 'file' ]]; then
            COMPREPLY=()
            compopt -o default
        elif [[ $type == 'plain' ]]; then
            COMPREPLY+=($value)
        fi
    done

    return 0
}

_charcoal_completion_setup() {
    complete -o nosort -F _charcoal_completion charcoal
    complete -o nosort -F _charcoal_completion gt
}

_charcoal_completion_setup
'''

ZSH_COMPLETION_SCRIPT = '''# Zsh completion for charcoal/gt
# To install: charcoal completion >> ~/.zshrc
# Or add to a file in your $fpath

#compdef charcoal gt

_charcoal_completion() {
    local -a completions
    local -a completions_with_descriptions
    local -a response
    (( ! $+commands[charcoal] )) && return 1

    response=("${(@f)$(env COMP_WORDS="${words[*]}" COMP_CWORD=$((CURRENT-1)) _CHARCOAL_COMPLETE=zsh_complete charcoal)}")

    for type key descr in ${response}; do
        if [[ "$type" == "plain" ]]; then
            if [[ "$descr" == "_" ]]; then
                completions+=("$key")
            else
                completions_with_descriptions+=("$key":"$descr")
            fi
        elif [[ "$type" == "dir" ]]; then
            _path_files -/
        elif [[ "$type" == "file" ]]; then
            _path_files -f
        fi
    done

    if [ -n "$completions_with_descriptions" ]; then
        _describe -V unsorted completions_with_descriptions -U
    fi

    if [ -n "$completions" ]; then
        compadd -U -V unsorted -a completions
    fi
}

if [[ $zsh_eval_context[-1] == loadautofunc ]]; then
    # autoload from fpath, call function directly
    _charcoal_completion "$@"
else
    # eval/source/. command, register function for later
    compdef _charcoal_completion charcoal
    compdef _charcoal_completion gt
fi
'''


@click.command()
@click.option(
    '--shell',
    type=click.Choice(['bash', 'zsh', 'fish'], case_sensitive=False),
    help='Shell type for completion script',
)
def completion(shell: str | None) -> None:
    """Set up bash or zsh tab completion.

    Generates shell completion scripts for the charcoal CLI. By default, attempts
    to detect the current shell from the SHELL environment variable.

    Installation:
        Bash: charcoal completion >> ~/.bash_completion
        Zsh:  charcoal completion >> ~/.zshrc
        Fish: charcoal fish >> ~/.config/fish/completions/gt.fish

    After adding the completion script, restart your shell or source the file.
    """
    if not shell:
        # Try to detect shell from environment
        shell_path = os.environ.get('SHELL', '')
        if 'bash' in shell_path:
            shell = 'bash'
        elif 'zsh' in shell_path:
            shell = 'zsh'
        elif 'fish' in shell_path:
            shell = 'fish'
        else:
            click.echo('Could not detect shell. Please specify --shell bash, --shell zsh, or --shell fish')
            return

    if shell == 'fish':
        click.echo('For Fish shell completion, use the "fish" command instead:')
        click.echo('  charcoal fish >> ~/.config/fish/completions/gt.fish')
        return

    if shell == 'bash':
        click.echo('# =============================================================================')
        click.echo('# Bash Completion Setup for Charcoal/GT')
        click.echo('# =============================================================================')
        click.echo('#')
        click.echo('# To enable completion, run ONE of the following:')
        click.echo('#')
        click.echo('# Option 1 (Recommended): Add to ~/.bash_completion')
        click.echo('#   charcoal completion --shell bash >> ~/.bash_completion')
        click.echo('#   source ~/.bash_completion')
        click.echo('#')
        click.echo('# Option 2: Add to ~/.bashrc')
        click.echo('#   charcoal completion --shell bash >> ~/.bashrc')
        click.echo('#   source ~/.bashrc')
        click.echo('#')
        click.echo('# =============================================================================')
        click.echo('')
        click.echo(BASH_COMPLETION_SCRIPT)
    elif shell == 'zsh':
        click.echo('# =============================================================================')
        click.echo('# Zsh Completion Setup for Charcoal/GT')
        click.echo('# =============================================================================')
        click.echo('#')
        click.echo('# To enable completion, run ONE of the following:')
        click.echo('#')
        click.echo('# Option 1 (Recommended): Add to ~/.zshrc')
        click.echo('#   charcoal completion --shell zsh >> ~/.zshrc')
        click.echo('#   source ~/.zshrc')
        click.echo('#')
        click.echo('# Option 2: Add to a file in your $fpath')
        click.echo('#   charcoal completion --shell zsh > /path/to/completions/_charcoal')
        click.echo('#')
        click.echo('# =============================================================================')
        click.echo('')
        click.echo(ZSH_COMPLETION_SCRIPT)
