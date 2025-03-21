# Stocks API

An API for managing stock purchases and monitoring stock market data using Python and FastAPI.

## 🚀 Technologies

- **Python 3.13**: Core programming language
- **FastAPI**: Modern web framework for building APIs
- **PostgreSQL**: Primary database
- **Redis**: Caching layer for stock data
- **Docker & Docker Compose**: Containerization and orchestration
- **Polygon.io**: Stock market data provider
- **SQLAlchemy**: SQL toolkit and ORM
- **Pydantic**: Data validation using Python type annotations
- **BeautifulSoup4**: HTML parsing

## 🔧 Prerequisites

- Make
- UV (python package and project manager) for tests and local running

The project can be run in two different ways, which have different dependencies.

### 🐳 Docker

- Docker and Docker Compose

### 🐍 Locally

- Python 3.13
- PostgreSQL database
- Redis server

## ⚙️ Environment Variables

Create a `.env` file based on `.env-template` with the following configurations:

| Variable | Description | Default Value |
|----------|-------------|---------------|
| REQUESTER_RETRY_MAX | Maximum number of request retries | 5 |
| REQUESTER_TIMEOUT | Request timeout in seconds | 20 |
| REQUESTER_ALLOW_REDIRECTS | Allow HTTP redirects | True |
| REQUESTER_STREAM | Enable request streaming | True |
| REQUESTER_VERIFY | SSL verification for requests | False |
| POLYGON_BASE_URL | Base URL for Polygon.io API | |
| POLYGON_API_KEY | API key for Polygon.io service | |
| DB_PROTOCOL | Database connection protocol | postgresql+psycopg |
| DB_USER | Database username | |
| DB_PASSWORD | Database password | |
| DB_HOST | Database host address | localhost |
| DB_PORT | Database port | 5432 |
| DB_NAME | Database name | |
| REDIS_URL | Redis connection URL | |
| CACHE_TTL_SECONDS | Cache time-to-live in seconds | 3600 |
| LOG_LEVEL | Application logging level | INFO |
| STOCK_DAILY_INFO_MAX_ATTEMPTS | Maximum attempts for fetching daily stock info | 5 |

## 🚀 Running the Project

1. Clone the repository:
```bash
git clone https://github.com/SillasReis/stocks-api.git
cd stocks-api
```

2. Set up environment variables:
```bash
cp .env-template .env
# Edit .env with your configurations
```

3. Start the services using Docker Compose:
```bash
make deploy
```
or
```bash
docker-compose up --build -d
```
The API will be available at `http://localhost:8000`.

4. Access the API documentation:
* Swagger: [http://localhost:8000/docs](http://localhost:8000/docs)
* ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## 🧪 Running Tests

```bash
make test
```
or
```bash
uv run python -m pytest tests/ -v
```

## 📦 Project Structure

- `src/`: Source code directory
  - `api/`: API layer
    - `routes/`: API endpoints and route handlers
  - `cacher/`: Caching implementation
  - `core/`: Core business logic and utilities
    - `stocks/`: Stock-related services and models
    - `utils.py`: Utility functions
  - `database/`: Database models and configuration
  - `polygon/`: Polygon.io API integration
  - `requester/`: HTTP request handling and configuration
  - `scraper/`: Web scraping modules
    - `marketwatch_stock/`: MarketWatch specific scraping
- `tests/`: Test suite

## 🥷 Developer

* **[Sillas Reis](https://github.com/SillasReis)**