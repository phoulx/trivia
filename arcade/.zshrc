# compatible with dev/dockerfile

HISTSIZE=100000
SAVEHIST=1000000

setopt histignorealldups sharehistory

# Use emacs keybindings even if our EDITOR is set to vi
bindkey -e

# The following lines were added by compinstall
autoload -Uz compinit
compinit

zstyle ':completion:*' matcher-list '' 'm:{a-z}={A-Z}' 'm:{a-zA-Z}={A-Za-z}' 'r:|[._-]=* r:|=* l:|=*'

# zsh extensions
source /usr/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
source /usr/share/zsh-autosuggestions/zsh-autosuggestions.zsh

export WORDCHARS=${WORDCHARS//[=\/]} 

# starship
eval "$(starship init zsh)"

# alias
alias ll='exa -l'
alias la='exa -laFh --time-style iso --icons --color-scale'
alias gs='git status'
alias python='python3'

