import create
import asyncio

from create import logger
from databases.database import DataBaseMain
DB_NAME = create.DB_NAME
DB_USER = create.DB_USER
DB_PASSWORD = create.DB_PASSWORD
DB_HOST = create.DB_HOST
DB_PORT = create.DB_PORT


async def main():
    print('start')
    db = DataBaseMain(db_user=DB_USER, db_password=DB_PASSWORD, db_host=DB_HOST, db_port=DB_PORT, db_name=DB_NAME, logger=logger)

    start = await db.start_db()
    print(f'start db = {start}')
    print(f'create user_1 = {await db.add_user_db(user_id=111, full_name="test_1", first_name="test_1")}')
    print(f'create user_2 = {await db.add_user_db(user_id=222, full_name="test_2", first_name="test_2")}')
    print(f'create user_3 = {await db.add_user_db(user_id=333, full_name="test_3", first_name="test_3")}')
    print(f'get user_2 = {await db.get_user_db(222)}')
    print(f'get not exist user = {await db.get_user_db(888)}')
    print(f'create request_1= {await db.add_request_db(111, "req_test", 15, True)}')
    print(f'get all users = {await db.get_all_users_db()}')
    print(f'get all requests = {await db.get_all_requests_db()}')
    print(f'get count req = {await db.get_requests_count_db()}')
    user = await db.get_user_db(111)
    print(f'get lang user_1 = {user.get("languageuser")}')
    print(f'get status admin user_1 = {user.get("statusadmin")}')
    print(f'get status ban user_1 = {user.get("is_banned")}')
    print(f'change lang user_2 = {await db.up_user_lang_db(222, "ru")}')
    print(f'change status admin user_2 = {await db.up_user_admin_db(222)}')
    print(f'banned user_2 = {await db.up_user_banned_db(222)}')
    print(f'get user_2 = {await db.get_user_db(222)}')
    print(f'get all users = {await db.get_all_users_db()}')
    print(f'change lang user_888 = {await db.up_user_lang_db(888, "ru")}')
    print(f'change status admin user_888 = {await db.up_user_admin_db(888)}')
    print(f'banned user_888 = {await db.up_user_banned_db(888)}')
    print(f'get user_888 = {await db.get_user_db(888)}')
    print(f'del user_222 = {await db.del_user_db(222)}')

    print('finish')

if __name__ == '__main__':

    asyncio.run(main())







