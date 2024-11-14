#!/bin/bash

# ANSI color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

while true
do
    # Print in red
    echo -e "${RED}Hello from service.sh!${NC}"

    # Print in green
    echo -e "${GREEN}Hello from service.sh!${NC}"

    # Print in blue
    echo -e "${BLUE}Hello from service.sh!${NC}"

    # Sleep for 5 seconds
    sleep 5

    # Execute the .py file
    python3 /workdir/cron_indexing_scheduler/indexing.py
done
