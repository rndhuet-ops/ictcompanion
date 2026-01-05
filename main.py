from fastapi import FastAPI, Request
import os
import requests

app = FastAPI()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

def send_telegram(text: str):
    if not BOT_TOKEN or not CHAT_ID:
        return
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": text}, timeout=10)

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/webhook")
async def webhook(req: Request):
    data = await req.json()
    event = data.get("event", "UNKNOWN")

    # Messages "pro" courts
    msg_map = {
        "H1_MSS_BULL": "MSS haussier en H1.\nCherche uniquement des longs.",
        "H1_MSS_BEAR": "MSS baissier en H1.\nCherche uniquement des shorts.",
        "M5_LIQUIDITY_TAKEN": "Liquidité prise.\nUn scénario devient possible.",
        "M5_MSS_DISPLACEMENT": "MSS confirmé avec displacement.\nOn attend un retour en zone.",
        "M5_FVG_CREATED": "FVG créée.\nZone prioritaire.",
        "M5_FVG_TOUCHED": "Retour dans la FVG.\nZone d’exécution possible.",
        "M5_OB_TOUCHED": "Retour sur un Order Block.\nZone secondaire.",
        "M5_BB_TOUCHED": "Retour sur un Breaker Block.\nZone avancée.",
        "INVALIDATION": "Scénario invalidé.\nOn attend un nouveau setup.",
    }

    text = msg_map.get(event, f"Event reçu: {event}")
    send_telegram(text)
    return {"status": "ok", "event": event}

