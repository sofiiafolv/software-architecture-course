#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <number_of_times_facades>"  
    exit 1
fi

FACADE_SERVICES_NUMBER="$1"

for ((i=1; i<=FACADE_SERVICES_NUMBER; i++)); do
    port=$((7000 + i))
    python facade-service/FacadeController.py 127.0.0.1 $port &
done

wait
