### Installation: charcoal fish >> ~/.config/fish/completions/gt.fish
### Or: charcoal fish >> ~/.config/fish/completions/charcoal.fish
# git helpers adapted from fish git completion
function __fish_git_local_branches
    command git for-each-ref --format='%(refname:strip=2)' refs/heads/ 2>/dev/null
end

function __fish_git_remote_branches
    command git for-each-ref --format="%(refname:strip=3)" refs/remotes/ 2>/dev/null
end

# disable file completions for the entire command
complete -c gt -f
complete -c charcoal -f

# commands that take branches
complete -c gt -x -n "__fish_seen_subcommand_from checkout co bco delete onto track untrack" -a "(__fish_git_local_branches)"
complete -c charcoal -x -n "__fish_seen_subcommand_from checkout co bco delete onto track untrack" -a "(__fish_git_local_branches)"

# gt/charcoal downstack get takes remote branches
complete -c gt -x -n "__fish_seen_subcommand_from downstack ds dsg" -n "__fish_seen_subcommand_from get dsg" -a "(__fish_git_remote_branches)"
complete -c charcoal -x -n "__fish_seen_subcommand_from downstack ds dsg" -n "__fish_seen_subcommand_from get dsg" -a "(__fish_git_remote_branches)"

# Initialize Click's completion system for charcoal and gt commands
# This enables dynamic completion for all commands using Click's protocol
eval (env _CHARCOAL_COMPLETE=fish_source charcoal 2>/dev/null)
eval (env _GT_COMPLETE=fish_source gt 2>/dev/null)
