import asyncpg
import os
import logging
from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone

from models import User
from utils import TOKEN_LIFETIME, hash_password

class RegistrationRepo:
    def __init__(self, pool: asyncpg.Pool):
        self.logger = logging.getLogger()
        self.pool = pool
        
    @classmethod
    async def initialize(cls)->asyncpg.Pool:
        try:
            pool = await asyncpg.create_pool(
                user = os.getenv('DB_USER'),
                password = os.getenv('DB_PASSWORD'),
                database = os.getenv('DB_NAME'),
                host = os.getenv('DB_HOST'),
                port = os.getenv('DB_PORT'),
                min_size=1,
                max_size=5
            )
            return pool
        except Exception as ex:
            logger = logging.getLogger()
            logger.error('Error connecting to database')
            raise ex
        
    async def close(self):
        try:
            await self.pool.close()
        except Exception as ex:
            self.logger.error('Error closing connection to database')
            raise ex

    async def check_if_exists(self, user: User)->bool:
        async with self.pool.acquire() as conn:
            cnt = await conn.fetchval(
                'SELECT COUNT(*) FROM Users WHERE usr_email = $1',
                user.email
            )
        return cnt > 0

    async def add_user(self, user: User, token):
        exists = await self.check_if_exists(user)
        if exists:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='User with this email already exists'
            )
        
        password_hash = hash_password(user.password)
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                try:
                    id = await conn.fetchval(
                        'INSERT INTO Users(usr_login, usr_email, usr_password_hash) VALUES ($1, $2, $3) RETURNING usr_id',
                        user.login, user.email, password_hash
                    )

                    await conn.execute(
                        'INSERT INTO Tokens (tkn_token, usr_id, tkn_expires_at) VALUES ($1, $2, $3)',
                        token, id, datetime.now(timezone.utc) + timedelta(seconds=TOKEN_LIFETIME)
                    )
                except Exception as ex:
                    self.logger.error('New user has not been added')
                    raise ex
                
    async def update_token(self, email: str, token):
        async with self.pool.acquire() as conn:
            try:
                id = await conn.fetchval(
                    'SELECT usr_id FROM Users WHERE usr_email = $1 AND NOT usr_is_verified',
                    email
                )

                if not id:
                    raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail='User with this email has already been verified or does not exists'
                )

                await conn.execute(
                    'UPDATE Tokens SET tkn_token = $1, tkn_expires_at = $2 WHERE usr_id = $3',
                    token, datetime.now(timezone.utc) + timedelta(seconds=TOKEN_LIFETIME), id
                )
            except Exception as ex:
                self.logger.error('Token has not been updated')
                raise ex
            
    async def verify_email(self, email: str, token: str)->bool:
        async with self.pool.acquire() as conn:
            try:
                id = await conn.fetchval(
                    '''SELECT u.usr_id 
                    FROM Users u 
                    JOIN Tokens t ON u.usr_id = t.usr_id 
                    WHERE u.usr_email = $1 AND t.tkn_token = $2 AND NOT u.usr_is_verified AND tkn_expires_at >= $3''',
                    email, token, datetime.now(timezone.utc)
                )

                if not id:
                    return False

                await conn.execute(
                    'UPDATE Users SET usr_is_verified = TRUE WHERE usr_id = $1',
                    id
                )
                return True

            except Exception as ex:
                self.logger.error('Email has not been verified')
                raise ex
            