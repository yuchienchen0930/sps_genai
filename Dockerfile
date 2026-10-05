# Use official Python image
FROM python:3.12-slim-bookworm

# Install curl (needed for uv installer)
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

# Install uv
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Add uv to PATH
ENV PATH="/root/.local/bin/:$PATH"

# Set working directory
WORKDIR /code

# Copy dependency files
COPY pyproject.toml uv.lock /code/

# Install dependencies (do NOT build project)
RUN uv sync --no-build --frozen

# Copy application code
COPY ./app /code/app

# Expose port
EXPOSE 8000

# Run FastAPI app
CMD ["uv", "run", "fastapi", "run", "app/main.py", "--port", "8000"]
