import requests
from fastapi import APIRouter, Request
from app.common.schemas import ValidationErrorLoggingRoute
from app.config import config

router = APIRouter(route_class=ValidationErrorLoggingRoute)

prefix = "/webhooks"
tags = ["webhooks"]


def send_telegram_message(text: str) -> None:
    if not config.TELEGRAM_BOT_TOKEN or not config.TELEGRAM_CHAT_ID:
        return
    url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": config.TELEGRAM_CHAT_ID, "text": text, "parse_mode": "HTML"}, timeout=10)


@router.post("/sentry")
async def sentry_webhook(request: Request):
    payload = await request.json()

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
