import os
import json
from fastapi import FastAPI

json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config", "config.json")
with open(json_path, "r") as config_file:
    config_data = json.load(config_file)

app = FastAPI(title=config_data["application"].get("title","FastAPI Peer to Peer Application"),
              description= config_data["application"].get("description","FastAPI Peer to Peer Application"),
              summary=config_data["application"].get("summary","FastAPI Peer to Peer Application"),
              version=config_data["application"].get("version","0.0.0")
              )


@app.get("/")
async def root():
    return {"message": "Hello World"}