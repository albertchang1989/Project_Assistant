from apscheduler.schedulers.background import BackgroundScheduler

from work_assistant.db import SessionLocal
from work_assistant.dingtalk.client import DingTalkClient
from work_assistant.repositories import WorkItemRepository
from work_assistant.services.report_service import ReportService


def send_morning_report(webhook: str) -> None:
    with SessionLocal() as session:
        report = ReportService(WorkItemRepository(session)).build_morning_report()
    DingTalkClient(webhook).send_text(report)


def send_evening_report(webhook: str) -> None:
    with SessionLocal() as session:
        report = ReportService(WorkItemRepository(session)).build_evening_report()
    DingTalkClient(webhook).send_text(report)


def build_scheduler(webhook: str) -> BackgroundScheduler:
    scheduler = BackgroundScheduler(timezone="Asia/Shanghai")
    scheduler.add_job(
        send_morning_report,
        "cron",
        day_of_week="mon-fri",
        hour=9,
        minute=30,
        args=[webhook],
    )
    scheduler.add_job(
        send_evening_report,
        "cron",
        day_of_week="mon-fri",
        hour=18,
        minute=30,
        args=[webhook],
    )
    return scheduler
