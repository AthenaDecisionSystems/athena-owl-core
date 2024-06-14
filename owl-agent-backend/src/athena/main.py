"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from athena.routers import conversations, documents, prompts, assistants, agents
from athena.app_settings import get_config
from dotenv import load_dotenv
import os
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # everything before yield is done before the app starts
    load_dotenv(dotenv_path=get_config().owl_env_path)
    yield
    # do something when app stop

app = FastAPI(lifespan=lifespan)

# List of authorized origins
origins = os.getenv("OWL_CLIENTS", ["http://localhost:3000"])


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(conversations.router)
app.include_router(documents.router)
app.include_router(prompts.router)
app.include_router(assistants.router)
app.include_router(agents.router)

@app.get(get_config().api_route + "/health")
def alive() -> dict[str,str]:
    return {"Status": "Alive"}

@app.get(get_config().api_route + "/version")
def version():
    return {"Version": get_config().version}