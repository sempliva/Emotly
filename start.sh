#!/bin/bash
if [ "$#" -lt 1 ]; then
    export EMOTLY_DB_NAME="emotly_db"
else if [ "$1" = "DEBUG" ]; then
    export EMOTLY_DB_NAME="emotly_db_test"
    else
        echo "$0 usage: $0 [DEBUG]"
        exit
    fi
fi

exec python3.5 emotly.py
