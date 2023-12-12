# LeapfrogAI Summarization Backend

## Description

Intermediate API that adds an agent specialized in tasks that require high-quality summarization.

## Usage

See [instructions](#instructions) to get the API up and running. Then, go to http://localhost:8081/docs for the Swagger documentation on API usage.

## Instructions

The instructions in this section assume the following:

1. Properly installed and configured Python 3.11.x, to include its development tools
2. You have filled out the `.env`, following the `.env.example`
3. You have the LeapfrogAI API or other OpenAI API compliant server that can be reached:
   - https://github.com/defenseunicorns/leapfrogai-api
   - **_NOTE:_** you need to use [this branch](https://github.com/defenseunicorns/leapfrogai-api/tree/add-completion-usage-placeholders) in order to workaround the LangChain usage compilation
4. You have chosen a LeapfrogAI model backend and have that running. Some examples of existing backends:
   - https://github.com/defenseunicorns/leapfrogai-backend-ctransformers
   - https://github.com/defenseunicorns/leapfrogai-backend-llama-cpp-python
   - **_NOTE:_** you need to use the _add-gpu-support_ branches on both backends to turn on GPU inferencing to accelerate the workflow and testing

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
