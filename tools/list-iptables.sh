#!/bin/bash

if [[ $EUID -ne 0 ]]
then
    echo "You must be root."
    exit 1
fi

TABLE="filter"

case "$1" in
    nat)
        TABLE="nat"
        ;;
    mangle)
        TABLE="mangle"
        ;;
    raw)
        TABLE="raw"
        ;;
    *)
esac

clear
/sbin/iptables -t "$TABLE" -L -n -v --line-numbers
