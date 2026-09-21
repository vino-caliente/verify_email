from fastapi import Request

from repositories.registration_repo import RegistrationRepo
from services.mail_service import EmailService
from services.registration_service import RegistrationService

def get_reg_repo(req: Request)->RegistrationRepo:
    return req.app.state.reg_repo

def get_mail_service(req: Request)->EmailService:
    return req.app.state.email_service

def get_reg_service(req: Request)->RegistrationService:
    return req.app.state.reg_service