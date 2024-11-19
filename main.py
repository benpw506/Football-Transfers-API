import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scraper import player_transfer_response
from dotenv import load_dotenv, dotenv_values

load_dotenv()

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins = [os.getenv("IP")],
    allow_credentials =True, 
    allow_methods = ["*"], 
    allow_headers=["*"]
    
)

@app.get("/")
def read():
    return {
        "msg": "Transfer Markt API"
    }

@app.get("/transfer/{transfer_id}")
def read(transfer_id : int):
    return player_transfer_response(transfer_id)

