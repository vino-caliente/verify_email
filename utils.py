from passlib.context import CryptContext
import secrets
from pathlib import Path

TOKEN_LIFETIME = 900 # 15 minutes

context = CryptContext(schemes=['bcrypt'])

def hash_password(passw: str)->str:
    return context.hash(passw)

def verify_password(passw, passw_hash):
    return context.verify(passw, passw_hash)

def get_token()->str:
    return secrets.token_urlsafe(32)

TEMPLATES_DIR = Path(__file__).parent / 'templates'
REG_PAGE = (TEMPLATES_DIR / 'reg_page.html').read_text(encoding='utf-8')
VERIFY_SUCCESS = (TEMPLATES_DIR / 'verify_success.html').read_text(encoding='utf-8')
VERIFY_CANCEL = (TEMPLATES_DIR /'verify_cancel.html').read_text(encoding='utf-8')