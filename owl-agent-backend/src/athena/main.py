"""
Copyright 2024 Athena Decision Systems
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from athena.routers import conversations, documents, prompts, agents, tools
from athena.app_settings import get_config, config_reload
from dotenv import load_dotenv
import os
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Actions before the app starts
    config = get_config()
    print(f"Owl Agent Backend v {config.version} starting ")
    print("Override env is set to: ", config.override_env)

    print("Loading application .env file at", config.owl_env_path)

    # Use load_dotenv with the override option from configuration
    load_dotenv(dotenv_path=config.owl_env_path, override=config.override_env)

    yield
    # Actions when the app stops
    print("Shutting down Owl Agent Backend")

app = FastAPI(lifespan=lifespan, redirect_slashes=False)

print("FastAPI will start with current directory =", os.getcwd())

# List of authorized origins
origins = os.getenv("OWL_CLIENTS", ["http://owl-frontend:3000,http://localhost:3000,http://localhost:3001"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(conversations.router)
app.include_router(documents.router)
app.include_router(prompts.router)
app.include_router(agents.router)
app.include_router(tools.router)

# Define health, version, and reload endpoints
@app.get(f"{config.api_route}/health", tags=["Server Info"])
def alive() -> dict[str, str]:
    return {"Status": "Alive"}

@app.get(f"{config.api_route}/version", tags=["Server Info"])
def version() -> dict[str, str]:
    return {"Version": config.version}

@app.put(f"{config.api_route}/reload", tags=["Server Info"])
def reload() -> str:
    return config_reload()
