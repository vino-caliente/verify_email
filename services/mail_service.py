from email.message import EmailMessage
import aiosmtplib
import os
import logging

class EmailService:
    def __init__(self):
        self.COMPANY_NAME = 'CoolCompany'
        self.DOMAIN_NAME = os.getenv("DOMAIN_NAME") or 'localhost:8000'

        self.logger = logging.getLogger()
    
    async def send_email(self, email: str, token: str):
        msg = EmailMessage()
        msg['From'] = os.getenv('SMTP_USER') or 'noreply@example.com'
        msg['To'] = email
        msg['Subject'] = f'Подтверждение email для {self.COMPANY_NAME}'

        content = f'''
Здравствуйте!

Для подтверждения email перейдите, пожалуйста, по ссылке ниже:

http://{self.DOMAIN_NAME}/api/registration/verify_email?token={token}&email={email}

С уважением, {self.COMPANY_NAME}
'''
        msg.set_content(content)

        try:
            # без username и password для локального запуска с mailpit
            await aiosmtplib.send(
                msg,
                hostname=os.getenv('SMTP_HOST'),
                port=int(os.getenv('SMTP_PORT')),
                username=os.getenv('SMTP_USER') or None,
                password=os.getenv('SMTP_PASSW') or None
            )
            self.logger.info(f'Email to {email} was sent')
        except Exception as ex:
            self.logger.error(f'Email to {email} was not sent')
            raise ex