"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from athena.routers import conversations, documents, prompts, agents, tools
from athena.app_settings import get_config, config_reload
from dotenv import load_dotenv, dotenv_values
import os
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # everything before yield is done before the app starts
    print(f"Owl Agent Backend v {get_config().version} starting ")

    # print("------ os.environ BEFORE ------")
    # for key in os.environ:
    #    print(key + " = " + os.environ[key])
    # print("------")

    print("Loading application .env file at", get_config().owl_env_path)

    # load_dotenv does not overwrite variables if they already exist
    # load_dotenv(dotenv_path=get_config().owl_env_path)
    config = dotenv_values(dotenv_path=get_config().owl_env_path)
    for key in config:
        os.environ[key] = config[key]

    # print("------ os.environ AFTER ------")
    # for key in os.environ:
    #    print(key + " = " + os.environ[key])
    # print("------")


    yield
    # do something when app stop

app = FastAPI(lifespan=lifespan)

print("FastAPI will start with current directory =", os.getcwd())

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
app.include_router(agents.router)
app.include_router(tools.router)

@app.get(get_config().api_route + "/health", tags=["Server Info"])
def alive() -> dict[str,str]:
    return {"Status": "Alive"}

@app.get(get_config().api_route + "/version", tags=["Server Info"])
def version() -> dict[str,str]:
    return {"Version": get_config().version}


@app.put(get_config().api_route + "/reload", tags=["Server Info"])
def reload() -> str:
    return config_reload()