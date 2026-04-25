FROM python:3.11-slim

WORKDIR /app

# Install API deps
COPY apps/api/requirements.txt ./requirements-api.txt
RUN pip install --no-cache-dir -r requirements-api.txt

# Install simulation engine deps
COPY requirements.txt ./requirements-sim.txt
RUN pip install --no-cache-dir -r requirements-sim.txt

# Copy simulation engine
COPY src/ ./src/

# Copy API source
COPY apps/api/ ./api/

WORKDIR /app/api
# /app is the repo root, so `import src.*` resolves relative imports correctly.
# The sim engine uses `from ..core.events` style, which requires src to be a package,
# not the root of sys.path.
ENV PYTHONPATH=/app

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
