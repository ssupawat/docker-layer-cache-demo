FROM python:3.12-slim

# Layer 1: system deps (rarely changes)
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Layer 2: python deps (changes only when requirements.txt changes)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Layer 3: source (changes most often)
COPY server.py .

EXPOSE 8000
CMD ["python", "server.py"]
