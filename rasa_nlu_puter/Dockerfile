# Use a Python container as a starting point
FROM python:3.7-slim

# Install dependencies of interest
RUN python -m pip install rasa[spacy] && \
    python -m spacy download en_core_web_lg

# Set workdir
WORKDIR /app
ENV HOME=/app

# Copy only necessary files
COPY . .

# Create 'models' directory with write permissions
# RUN mkdir -p models && chown -R 1001:1001 models


# Train a new Rasa model
RUN rasa train nlu

# Set the user to run, don't run as root
USER 1001

# Set entrypoint for interactive shells
ENTRYPOINT ["rasa"]

# Command to run when container is called to run
CMD ["run", "--enable-api", "--port", "8080"]
