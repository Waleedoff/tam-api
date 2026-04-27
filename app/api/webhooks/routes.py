import requests
from fastapi import APIRouter, Request
from app.common.schemas import ValidationErrorLoggingRoute
from app.config import config

router = APIRouter(route_class=ValidationErrorLoggingRoute)

prefix = "/webhooks"
tags = ["webhooks"]


def send_telegram_message(text: str):
    if not config.TELEGRAM_BOT_TOKEN or not config.TELEGRAM_CHAT_ID:
        return "missing env vars"
    url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
    resp = requests.post(url, json={"chat_id": config.TELEGRAM_CHAT_ID, "text": text, "parse_mode": "HTML"}, timeout=10)
    return resp.json()


@router.post("/test-telegram")
def test_telegram():
    result = send_telegram_message("✅ TAM API Telegram test - working!")
    return {"bot_token_set": bool(config.TELEGRAM_BOT_TOKEN), "chat_id_set": bool(config.TELEGRAM_CHAT_ID), "result": result}


@router.post("/sentry")
async def sentry_webhook(request: Request):
    body = await request.body()
    if not body:
        return {"ok": True}
    try:
        payload = await request.json()
    except Exception:
        return {"ok": True}

    action = payload.get("action", "")
    data = payload.get("data", {})
    issue = data.get("issue", {})

    title = issue.get("title", "Unknown error")
    level = issue.get("level", "error").upper()
    project = payload.get("project", "")
    url = issue.get("permalink", "")
    times_seen = issue.get("times_seen", 1)

    text = (
        f"🚨 <b>Sentry Alert</b>\n"
        f"<b>Project:</b> {project}\n"
        f"<b>Level:</b> {level}\n"
        f"<b>Action:</b> {action}\n"
        f"<b>Error:</b> {title}\n"
        f"<b>Occurrences:</b> {times_seen}\n"
    )
    if url:
        text += f"<b>Link:</b> {url}"

    send_telegram_message(text)
    return {"ok": True}
