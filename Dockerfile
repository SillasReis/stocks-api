FROM python:3.13-slim-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

ADD https://astral.sh/uv/0.6.9/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin/:$PATH"

WORKDIR /app

COPY .env .gitignore pyproject.toml README.md uv.lock .python-version /app/
COPY src /app/src

RUN uv sync --frozen && uv pip install -e .

CMD ["uv", "run", "gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-b", ":8000", "src.api:app"]
