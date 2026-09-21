from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from pydantic import EmailStr

from models import User, ResendEmail
from services.registration_service import RegistrationService
from dependencies import get_reg_service
from utils import REG_PAGE, VERIFY_SUCCESS, VERIFY_CANCEL

reg_router = APIRouter(
    prefix='/registration'
)

@reg_router.get('/')
def get_reg_page():
    return HTMLResponse(REG_PAGE)

@reg_router.post('/new_user')
async def add_user(
        user: User, 
        reg_service: RegistrationService = Depends(get_reg_service)
    ):
    await reg_service.add_user(user)
    return {'status': 'ok', 'details': 'user added'}

@reg_router.patch('/resend_email')
async def resend_email(
        resend_email: ResendEmail,
        reg_service: RegistrationService = Depends(get_reg_service)
    ):
    await reg_service.resend_email(resend_email.email)
    return {'status': 'ok', 'details': 'email resended'}

@reg_router.get('/verify_email')
async def verify_email(
    token: str, 
    email: EmailStr, 
    reg_service: RegistrationService = Depends(get_reg_service)
    ):
    was_verified = await reg_service.verify_email(email, token)
    return HTMLResponse(VERIFY_SUCCESS if was_verified else VERIFY_CANCEL)