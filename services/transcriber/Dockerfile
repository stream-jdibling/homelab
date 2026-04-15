FROM nvidia/cuda:12.8.0-runtime-ubuntu24.04

RUN apt-get update && apt-get install -y \
    python3 python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install faster-whisper fastapi uvicorn --break-system-packages

WORKDIR /app

COPY main.py .

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]