import os
from contextlib import asynccontextmanager
import json
from fastapi import FastAPI
from database import engine
from routes import (UserRouter,
                   AuthRouter,
                   AccountRouter,
                   TransactionRouter,
                   MiscellaneousRouter)


json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config", "config.json")
with open(json_path, "r") as config_file:
    config_data = json.load(config_file)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: (Optional) Place migration or connection test code here
    yield
    # Shutdown: Dispose of engine (close DB connections)
    await engine.dispose()


app = FastAPI(title=config_data["application"].get("title","FastAPI Peer to Peer Application"),
              description= config_data["application"].get("description","FastAPI Peer to Peer Application"),
              summary=config_data["application"].get("summary","FastAPI Peer to Peer Application"),
              version=config_data["application"].get("version","0.0.0")
              )

app.include_router(router=UserRouter, tags=["Users"])
app.include_router(router=AuthRouter, tags=["Authentication","Users"])
app.include_router(router=MiscellaneousRouter, tags=["Transactions","Miscellaneous"])
app.include_router(router=AccountRouter, tags=["Accounts"])