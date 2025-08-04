# Mythical Creatures API

A FastAPI-based REST API for managing mythical creatures and their realms.

## Setup

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the server:

```bash
uvicorn main:app --reload --port 8080
```

## API Documentation

Once the server is running, visit:

-   Swagger UI: http://127.0.0.1:8080/docs
-   ReDoc: http://127.0.0.1:8080/redoc

## Testing

Run tests with:

```bash
pytest -q
```
