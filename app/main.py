from fastapi import FastAPI #Imports the FastAPI class to create our web application.
from app.routes import router #Imports the CRUD endpoints (POST /items, GET /items, etc.) from routes.py.
from app.metrics import metrics_middleware, metrics_endpoint #Imports the Prometheus /metrics endpoint, so your app can be monitored.
from app.db import engine, Base

# create the fast API, Creates the app instance.
# title and version are metadata useful in Swagger UI (/docs).
app = FastAPI(title="Cloud Centric Application", version="0.0.1")


# Create DB tables on startup (DEV ONLY)
# # Auto-creating tables is OK for local development, NOT for production.
# @app.on_event("startup")
# def startup_event():
# Base.metadata.create_all(bind=engine)

# register custom HTTP middleware in a FastAPI application
# app.middleware("http"): This is a decorator that tells FastAPI to run the following function for every incoming HTTP request.
# the execution flow:
# A request hits the server
# the metrics_middleware logic starts
# the request is passed to the actual route (the "next" call)
# the response comes back
# the middleware finishes
app.middleware("http")(metrics_middleware)

# include application routes 
# Registers your main CRUD routes with the app.
# fast API use routers to organize endpoints
# router handles main API endpoints
#  This is used for Modular Organization. You use this to plug in a collection of routes (an APIRouter) that you defined in a separate file (like your app/routes.py).
app.include_router(router)

#include prometheus metrics router
# Registers /metrics endpoint for Prometheus scraping.
# This is a Lower-Level Manual Registration. It is the programmatic equivalent of using the @app.get("/metrics") decorator.
# Directly links a specific URL path to a specific Python function
app.add_api_route("/metrics", metrics_endpoint)

#healthcheck endpoint for kubernetes redinedd/liveness probes
# Kubernetes uses it to check if the pod is alive and ready.
@app.get("/health")
def health():
    # Returns simple JSON:
    return {"status":"ok"}

