from aiogram.fsm.state import StatesGroup, State

from config import token, channel, admin_user, admins, amount_per_one, minimal_vivod, usd_or_rub, currency
import aiosqlite
from config import *


# Пользовательские классы
class withdrawal_of_balance(StatesGroup):
    withdrawal_amount_state = State()


# Админ классы
class receiving_a_message(StatesGroup):
    receiving_message_state = State()


class private_message(StatesGroup):
    id_or_username_state = State()
    private_message_state = State()


class changing_the_balance(StatesGroup):
    id_or_username_state = State()
    change_amount_state = State()


# Создание базы данных
async def create_database():
    async with aiosqlite.connect("database2.db") as db2:
        await db2.execute("""CREATE TABLE IF NOT EXISTS database(
                            basic_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            user_id BIGINT NOT NULL,
                            user_balance DECIMAL DEFAULT 0,
                            user_username TEXT,
                            referrer_id INTEGER,
                            referrer_bonus INTEGER DEFAULT 0,
                            karta TEXT NULL,
                            entry_date DATE)""")
        await db2.commit()


# Изменение номера карты 
async def add_karta(user_id, karta):
    async with aiosqlite.connect('database2.db') as db2:
        await db2.execute("UPDATE database SET karta = ? WHERE user_id = ?", (karta, user_id))
        await db2.commit()


# Получение номера карты по user_id
async def get_kard_number(user_id):
    async with aiosqlite.connect('database2.db') as db2:
        async with db2.execute('SELECT karta FROM database WHERE user_id = ?', (user_id,)) as cursor:
            kard_number = await cursor.fetchall()
            return kard_number


# Добавление данных
async def adding_data(user_id, user_username, referrer, referrer_bonus, entry_date):
    async with aiosqlite.connect("database2.db") as db2:
        await db2.execute(
            "INSERT INTO database (user_id, user_username, user_balance, referrer_id, referrer_bonus, entry_date) VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, user_username, 0, referrer, referrer_bonus, entry_date))
        await db2.commit()


# Выбор всех пользователей бд
async def select_all_user_id():
    async with aiosqlite.connect("database2.db") as db2:
        async with db2.execute("SELECT user_id FROM database") as cursor:
            all_users = await cursor.fetchall()
            return all_users


# Выбор определенной записи по user_id
async def select_user_id_where_user_id(user_id):
    async with aiosqlite.connect("database2.db") as db2:
        async with db2.execute("SELECT user_id FROM database WHERE user_id = ?", (user_id,)) as cursor:
            user_id = await cursor.fetchone()
            return user_id


# Выбор определенного значения столбца
async def select_user_username_where_user_name(user_username):
    async with aiosqlite.connect("database2.db") as db2:
        async with db2.execute("SELECT user_username FROM database WHERE user_username = ?",
                               (user_username,)) as cursor:
            user_username = await cursor.fetchone()
            return user_username[0]


# Выбор определенного значения столбца
async def select_user_id_where_user_username(user_username):
    async with aiosqlite.connect("database2.db") as db2:
        async with db2.execute("SELECT user_id FROM database WHERE user_username = ?", (user_username,)) as cursor:
            user_id = await cursor.fetchone()
            return user_id[0]


# Выбор определенного значения столбца
async def select_entry_date_where_user_id(user_id):
    async with aiosqlite.connect("database2.db") as db2:
        async with db2.execute("SELECT entry_date FROM database WHERE user_id = ?", (user_id,)) as cursor:
            entry_date = await cursor.fetchone()
            return entry_date[0]


# Выбор определенного значения столбца
async def select_user_balance_where_user_id(user_id):
    async with aiosqlite.connect("database2.db") as db2:
        async with db2.execute("SELECT user_balance FROM database WHERE user_id = ?", (user_id,)) as cursor:
            user_balance = await cursor.fetchone()
            return user_balance[0]



# Выбор определенного значения столбца
async def select_referrer_id_where_user_id(user_id):
    async with aiosqlite.connect("database2.db") as db2:
        async with db2.execute("SELECT referrer_id FROM database WHERE user_id = ?", (user_id,)) as cursor:
            referral = await cursor.fetchone()
            return referral[0]


# Выбор определенного значения столбца
async def select_referrer_bonus_where_user_id(user_id):
    async with aiosqlite.connect("database2.db") as db2:
        async with db2.execute("SELECT referrer_bonus FROM database WHERE user_id = ?", (user_id,)) as cursor:
            referrer_bonus = await cursor.fetchone()
            return referrer_bonus[0]

# Вывод общего количества рефералов
async def select_user_id_where_referrer_id_and_referrer_bonus_1(user_id):
    async with aiosqlite.connect("database2.db") as db2:
        async with db2.execute("SELECT user_id FROM database WHERE referrer_id = ? AND referrer_bonus = 1",
                               (user_id,)) as cursor:
            number_referrals = await cursor.fetchall()
            return number_referrals


# Изменение user_name в таблице
async def changing_username_where_user_id(user_username, user_id):
    async with aiosqlite.connect("database2.db") as db2:
        await db2.execute("UPDATE database SET user_username = ? WHERE user_id = ?", (user_username, user_id))
        await db2.commit()


# Изменение суммы начисления баланса за одного реферала
async def changing_referrer_bonus_where_user_id(referrer_bonus, user_id):
    async with aiosqlite.connect("database2.db") as db2:
        await db2.execute("UPDATE database SET referrer_bonus = ? WHERE user_id = ?", (referrer_bonus, user_id))
        await db2.commit()


# Изменение баланса пользователя
async def changing_user_balance_where_user_id(change_amount, username_or_id):
    async with aiosqlite.connect("database2.db") as db2:
        await db2.execute("UPDATE database SET user_balance = ? WHERE user_id = ?", (change_amount, username_or_id))
        await db2.commit()


# Добавление баланса пользователю
async def adding_user_balance_where_user_id(referral):
    async with aiosqlite.connect("database2.db") as db2:
        await db2.execute("UPDATE database SET user_balance = user_balance + ? WHERE user_id = ?",
                         (amount_per_one, referral,))
        await db2.commit()
