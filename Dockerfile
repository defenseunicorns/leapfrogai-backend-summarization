ARG ARCH=amd64

FROM ghcr.io/defenseunicorns/leapfrogai/python:3.11-dev-${ARCH} as builder

WORKDIR /leapfrogai

COPY requirements.txt .
COPY scripts/download_gpt2.py .

RUN pip install -r requirements.txt --user 
RUN python scripts/download_gpt2.py

FROM ghcr.io/defenseunicorns/leapfrogai/python:3.11-${ARCH}

WORKDIR /leapfrogai

COPY --from=builder /home/nonroot/.local/lib/python3.11/site-packages /home/nonroot/.local/lib/python3.11/site-packages
COPY --from=builder /home/nonroot/.local/bin/uvicorn /home/nonroot/.local/bin/uvicorn
COPY --from=builder /leapfrogai/.model .

COPY main.py .
COPY backends/ backends/

EXPOSE 8080

ENTRYPOINT ["/home/nonroot/.local/bin/uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8081", "--log-config=log_config.yaml"]