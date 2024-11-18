
from fastapi import FastAPI
import uvicorn
from scraper import player_transfer_response

app = FastAPI()

@app.get("/")
def read():
    return {
        "msg": "Transfer Markt API"
    }

@app.get("/transfer/{transfer_id}")
def read(transfer_id : int):
    return player_transfer_response(transfer_id)

""" if __name__ == "__main__":
    uvicorn.run(app, port=8000)
 """