#!/bin/bash

# requirements example
req="zcat git gaga cat tar ls dasd top"

function check_req {
    err_flag=false
    for prog_name in $@
    do
        if ! which $prog_name 1>/dev/null
        then
            err_flag=true
            echo "Not found: $prog_name"
        fi
    done
    if [ "$err_flag" = true ]
    then
        exit 1
    fi
}

check_req $req
