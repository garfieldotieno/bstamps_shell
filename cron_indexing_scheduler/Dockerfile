# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory to /cron_indexing_scheduler
WORKDIR /cron_indexing_scheduler

# Copy the current directory contents into the container at /cron_indexing_scheduler
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run service.sh when the container launches
CMD ["./service.sh"]
