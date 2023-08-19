"""This module contains the class for admin response."""
from aiogram import types
from admin import smtp
from datetime import datetime
from create import LOG_FILE, db, logger
from asyncpg import Record


class AdminResponse:
    def __init__(self, message: types.Message):
        self.message = message

    async def send_log(self):
        """Send log file to admin in telegram."""
        try:
            with open(LOG_FILE, 'rb') as file:
                await self.message.answer_document(file)
        except FileNotFoundError as e:
            logger.exception(f'Error: {str(e)}')
            await self.message.answer('Log file not found')
        except Exception as e:
            logger.exception(f'Error: {str(e)}')
            await self.message.answer('Error send log file')

    async def send_email_lod(self):
        """Send log file to admin in email."""
        subject = f'Log file by {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
        if smtp.send_email(subject=subject, file=LOG_FILE, attach_file=True, logger=logger):
            await self.message.answer('Log file send to email')
        else:
            await self.message.answer('Error send log file to email')

    async def send_users(self):
        """Send id and users of this chat to admin."""
        _users: list[Record] = await db.get_all_users_db()
        if not _users:
            await self.message.answer('Users not found')
            return
        for user in _users:
            await self.message.answer(f'id= {user.get("userid")} name: {user.get("firstname")}')
        await self.message.answer('It is done')

    async def send_requests(self):
        """Send number of requests to admin."""
        _requests = await db.get_requests_count_db()
        await self.message.answer(f'Number of  requests is {_requests}')


if __name__ == '__main__':
    pass
