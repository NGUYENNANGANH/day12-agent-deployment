# Stage 1: Build
FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .

# Install dependencies into a virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Stage 2: Run
FROM python:3.11-slim

WORKDIR /app
# Copy the virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY app /app/app

# Don't run as root
RUN useradd -m -r agentuser
USER agentuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]
