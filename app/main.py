import os
from contextlib import asynccontextmanager
import json
from fastapi import FastAPI, Request,status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import OperationalError
from database import engine
from sqlalchemy.exc import SQLAlchemyError
import logging
import socket
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
              version=config_data["application"].get("version","1.0.0")
              )

app.include_router(router=UserRouter, tags=["Users"])
app.include_router(router=AuthRouter, tags=["Authentication","Users"])
app.include_router(router=MiscellaneousRouter, tags=["Transactions","Miscellaneous"])
app.include_router(router=AccountRouter, tags=["Accounts"])
app.include_router(router=TransactionRouter, tags=["Transactions"])

# Set up logging
logger = logging.getLogger(__name__)

@app.exception_handler(socket.gaierror)
async def gaierror_exception_handler(request: Request, exc: socket.gaierror):
    logger.exception("Global socket.gaierror caught: %s", exc)
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"detail": "A network resolution error to Database or External API occurred. Please check connectivity or try again later."},
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.exception("An unhandled exception occurred: %s", exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected server error occurred."},
    )
