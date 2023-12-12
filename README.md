# LeapfrogAI Summarization Backend

## Description

Backend API that adds a specific agent for tasks related to summarization.

## Usage

See [instructions](#instructions) to get the API up and running. Then, go to http://localhost:8081/docs for the Swagger documentation on API usage.

## Instructions

The instructions in this section assume the following:

1. Properly installed and configured Python 3.11.x, to include its development tools
2. You have filled out the `.env`, following the `.env.example`
2. You have the LeapfrogAI API or other OpenAI API compliant server that can be reached:
   - https://github.com/defenseunicorns/leapfrogai-api
3. You have chosen a LeapfrogAI model backend and have that running. Some examples of existing backends:
   - https://github.com/defenseunicorns/leapfrogai-backend-ctransformers
   - https://github.com/defenseunicorns/leapfrogai-backend-whisper

### Local Development

For locally running the development backend.

```bash
# Setup Python Virtual Environment
make create-venv
make activate-venv
make requirements-dev

# Start Model Backend
make dev
```

### Docker Container

#### Image Build and Run

For local image building and running.

```bash
# Build the docker image
docker build -t ghcr.io/defenseunicorns/leapfrogai/summarization:latest .

# Run the docker container
docker run -p 8080:8080 -v ./.env:/leapfrogai/.env ghcr.io/defenseunicorns/leapfrogai/summarization:latest
```
