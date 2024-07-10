# Building Microservices with FastAPI and Docker 🚀

To enable communication between microservices using FastAPI, we'll expand on the previous example and demonstrate how `service2` can make a request to `service1` using HTTP and also include some emoji fun along the way! Let's walk through the steps:

## 1. Setting Up `service1`

Let's create a simple `service1` that responds with a greeting message:

```python
# service1.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/service1/")
async def read_service1():
    return {"message": "👋 Hello from Service 1 🚀"}
```

## 2. Setting Up `service2`

Now, `service2` will make a request to `service1` to fetch its response and combine it with its own:

```python
# service2.py
from fastapi import FastAPI
import httpx

app = FastAPI()

@app.get("/service2/")
async def read_service2():
    # Make a request to Service 1
    async with httpx.AsyncClient() as client:
        response = await client.get("http://service1:8000/service1/")

    service1_message = response.json()["message"]

    return {"message": f"👋 Hello from Service 2! 🚀 {service1_message}"}
```

## 3. Docker Configuration with Docker Compose

Create Dockerfiles for both services and a `docker-compose.yml` file to orchestrate them together:

## Dockerfile for `service1`

```dockerfile
# Dockerfile for service1
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY ./service1 /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["uvicorn", "service1:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Dockerfile for `service2`:

```dockerfile
# Dockerfile for service2
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY ./service2 /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["uvicorn", "service2:app", "--host", "0.0.0.0", "--port", "8000"]
```

## `docker-compose.yml` to orchestrate both services:

```yaml
version: "3"
services:
  service1:
    build:
      context: ./service1
    ports:
      - "8000:8000"
  service2:
    build:
      context: ./service2
    ports:
      - "8001:8000"
    depends_on:
      - service1
```

## 4. Running the Microservices

- Build and start the services using Docker Compose:

  ```bash
  docker-compose up --build
  ```

- Access the services:
  - `service1` will be accessible at: `http://localhost:8000/service1/`
  - `service2` will be accessible at: `http://localhost:8001/service2/`

## Summary

- **Communication**: `service2` makes an HTTP request to `service1` to fetch its response and combines it with its own response.
- **Deployment**: Dockerize each FastAPI microservice and orchestrate them using Docker Compose.
- **Fun with Emojis**: Added some emojis to the responses for fun and clarity!

This setup demonstrates a basic communication pattern between microservices using FastAPI and Docker, suitable for local development or deployment in a containerized environment. Adjust ports and network configurations as needed for different environments or deployment strategies.

---
