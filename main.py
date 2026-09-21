from fastapi import FastAPI
from contextlib import asynccontextmanager

from repositories.registration_repo import RegistrationRepo
from services.registration_service import RegistrationService
from services.mail_service import EmailService
from api.registration_router import reg_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.pool = await RegistrationRepo.initialize()
    app.state.reg_repo = RegistrationRepo(app.state.pool)
    app.state.email_service = EmailService()
    app.state.reg_service = RegistrationService(app.state.reg_repo, app.state.email_service)

    yield

    await app.state.reg_repo.close()

app = FastAPI(lifespan=lifespan)

app.include_router(reg_router, prefix='/api')