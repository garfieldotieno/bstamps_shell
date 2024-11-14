#!/bin/sh

# Sleep for a random duration between 1 and 5 seconds
sleep $(((RANDOM % 5) + 1))s

# Update packages and install necessary dependencies
apk update
apk add --no-cache docker-cli

# Check if the Redis container is running
CONTAINER_STATUS=$(docker inspect -f '{{.State.Running}}' bstamps_shell-bredis-1)

if [ "$CONTAINER_STATUS" = "true" ]; then
    # Check if keys are empty in database 3
    KEY_COUNT_BEFORE=$(docker exec bstamps_shell-bredis-1 redis-cli -n 3 DBSIZE)

    if [ "$KEY_COUNT_BEFORE" -eq 0 ]; then
        # Fetch the data from the AOF file
        docker exec bstamps_shell-bredis-1 sh -c 'redis-cli -n 3 --pipe < /data/appendonly.aof'
        echo "Data reloaded from AOF file to database 3."

        # Check the number of keys after reloading
        KEY_COUNT_AFTER=$(docker exec bstamps_shell-bredis-1 redis-cli -n 3 DBSIZE)
        echo "Number of keys in database 3 before reloading: $KEY_COUNT_BEFORE."
        echo "Number of keys in database 3 after reloading: $KEY_COUNT_AFTER."
    else
        echo "Keys are not empty in database 3 before reloading. No action taken."
        echo "Number of keys in database 3: $KEY_COUNT_BEFORE."
    fi
else
    echo "Redis container is not running. No action taken."
fi

# Add any additional commands or actions as necessary
