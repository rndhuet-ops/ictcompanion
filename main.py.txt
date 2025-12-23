from fastapi import FastAPI, Request
import requests
import os

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

app = FastAPI()

state = "WAIT_LIQUIDITY"

def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": msg})

@app.post("/webhook")
async def webhook(req: Request):
    global state
    data = await req.json()
    event = data.get("event")

    if event == "SWEEP" and state == "WAIT_LIQUIDITY":
        state = "WAIT_STRUCTURE"
        send("La liquidité vient d’être prise.\nOn attend un changement de structure.")

    elif event in ["CHOCH", "BOS"] and state == "WAIT_STRUCTURE":
        state = "WAIT_ZONE"
        send("La structure change.\nOn attend un retour en zone.")

    elif event in ["FVG", "OB", "BB"] and state == "WAIT_ZONE":
        send("Le prix est dans une zone intéressante.\nObserve la réaction.")

    return {"status": "ok"}
