#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

PS1='[\u@\h \W]\$ '

shopt -s autocd
export HISTCONTROL=ignoredups

# Aliases
alias 3clear='clear; clear; clear'
alias pacman='sudo pacman'
alias ls='ls --color=auto'
alias grep='grep --color=auto'
alias cddjango='cd /usr/lib64/python3.6/site-packages/django/'
