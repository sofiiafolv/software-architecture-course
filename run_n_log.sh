#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <number_of_times_log>"  
    exit 1
fi

LOGGING_SERVICES_NUMBER="$1"

for ((i=1; i<=LOGGING_SERVICES_NUMBER; i++)); do
    port=$((8000 + i))
    python logging-service/LoggingController.py 127.0.0.1 $port &
done

wait
