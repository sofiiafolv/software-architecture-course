#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <number_of_times_msg>"  
    exit 1
fi

MESSAGES_SERVICES_NUMBER="$1"

for ((i=1; i<=MESSAGES_SERVICES_NUMBER; i++)); do
    port=$((9081 + i))
    python messages-service/MessagesController.py $port &
done

wait
