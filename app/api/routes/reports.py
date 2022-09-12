from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.image_status import ImageStatus
from app.repositories.user import user_repo
from app.api.dependencies.db.db import get_db
from app.models.user import User





router = APIRouter()


@router.get("/reviewers_report")
def get_reviewers_report(id: int, db: Session = Depends(get_db)):

    reviewers = db.query(User).filter(User.user_role == "reviewer").all()
    reports = []
    for reviewer in reviewers:
        report = {"reviewer": reviewer, "report": {"good": 30,
                                                   "rejected": "40", "cropped": 30, "sent_for_download": 43}}
        reports.append(report)
    return {
        "report": reports
    }


@router.get("/reviewers_report_by_date")
def get_reviewers_report(id: int, db: Session = Depends(get_db)):

    reviewers = db.query(User).filter(User.user_role == "reviewer").all()
    reports = []
    for reviewer in reviewers:
        report = {"reviewer": reviewer, "report": {"good": 30,
                                                   "rejected": "40", "cropped": 30, "sent_for_download": 43}}
        reports.append(report)
    return {
        "report": reports
    }


@router.get("/single_reviewer_report_by_date")
def get_reviewers_report(id: int, db: Session = Depends(get_db)):

    reviewers = db.query(User).filter(User.user_role == "reviewer").all()
    reports = []
    for reviewer in reviewers:
        report = {"reviewer": reviewer, "report": {"good": 30,
                                                   "rejected": "40", "cropped": 30, "sent_for_download": 43}}
        reports.append(report)
    return {
        "report": reports
    }


@router.get("/editors_report")
def get_editors_report(id: int, db: Session = Depends(get_db)):

    reviewers = db.query(User).filter(User.user_role == "reviewer").all()
    reports = []
    for reviewer in reviewers:
        report = {"reviewer": reviewer, "report": {"good": 30,
                                                   "rejected": "40", "cropped": 30, "sent_for_download": 43}}
        reports.append(report)
    return {
        "report": reports
    }


@router.get("/editors_report_by_date")
def get_editors_report_by_date(id: int, db: Session = Depends(get_db)):

    reviewers = db.query(User).filter(User.user_role == "reviewer").all()
    reports = []
    for reviewer in reviewers:
        report = {"reviewer": reviewer, "report": {"good": 30,
                                                   "rejected": "40", "cropped": 30, "sent_for_download": 43}}
        reports.append(report)
    return {
        "report": reports
    }


@router.get("/single_editors_report_by_date")
def get_single_editors_report_by_date(id: int, db: Session = Depends(get_db)):

    reviewers = db.query(User).filter(User.user_role == "reviewer").all()
    reports = []
    for reviewer in reviewers:
        report = {"reviewer": reviewer, "report": {"good": 30,
                                                   "rejected": "40", "cropped": 30, "sent_for_download": 43}}
        reports.append(report)
    return {
        "report": reports
    }
