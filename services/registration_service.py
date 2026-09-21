from repositories.registration_repo import RegistrationRepo
from services.mail_service import EmailService
from models import User
from utils import get_token

class RegistrationService:
    def __init__(self, reg_repo: RegistrationRepo, email_service: EmailService):
        self.reg_repo = reg_repo
        self.email_service = email_service

    async def add_user(self, user: User):
        token = get_token()
        await self.reg_repo.add_user(user, token)
        await self.email_service.send_email(user.email, token)

    async def resend_email(self, email: str):
        token = get_token()
        await self.reg_repo.update_token(email, token)
        await self.email_service.send_email(email, token)
    
    async def verify_email(self, email: str, token: str)->bool:
        return await self.reg_repo.verify_email(email, token)
