FROM alpine:3.16

# Install necessary packages
RUN apk update && \
    apk add --no-cache docker-cli

# Copy the script to the container
COPY redis_data_loader.sh /cron_redis_loader/redis_data_loader.sh

# Set the script as executable
RUN chmod +x /cron_redis_loader/redis_data_loader.sh

# Set the working directory
WORKDIR /cron_redis_loader

# Set the entry point to the script
CMD ["sh", "-c", "/cron_redis_loader/redis_data_loader.sh"]
