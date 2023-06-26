
from db import select_user_id_where_referrer_id_and_referrer_bonus_1, select_entry_date_where_user_id, \
    select_user_balance_where_user_id, select_user_id_where_user_id, adding_data, changing_username_where_user_id, \
    withdrawal_of_balance, select_referrer_bonus_where_user_id, select_referrer_id_where_user_id, \
    adding_user_balance_where_user_id, changing_referrer_bonus_where_user_id, changing_user_balance_where_user_id, \
    select_all_user_id, private_message, receiving_a_message, changing_the_balance, \
    select_user_username_where_user_name, select_user_id_where_user_username, changing_user_balance_where_user_username, \
    create_database, add_karta, get_kard_number
from loader import router
from aiogram.filters.command import Command
from aiogram.filters.text import Text
from aiogram.types import Message, CallbackQuery

from config import currency, usd_or_rub, admins_id, minimal_vivod, amount_per_one, \
    channel, admin_user
from keyboards import inline_kb1, default_kb2, update_follow_menu_keyboard, \
    default_kb99, \
    default_kb23, inline_kb24, inline_kb26, default_kb81
from state import Zaim, Karta

from loader import bot
import datetime

from decimal import Decimal

import requests
from aiogram import types
from aiogram.fsm.context import FSMContext


def check_sub_channel(chat_member):
    print(chat_member.status)
    if chat_member.status != 'left':
        return True
    else:
        return False


@router.message(Command('start'))
async def command_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await create_database()
    user_id = message.from_user.id
    user_username = message.from_user.username
    if await select_user_id_where_user_id(user_id) is None:
        try:
            referrer = int(message.text.split()[1])
            if user_id != referrer:
                referrer_bonus = 0
            else:
                referrer = None
                referrer_bonus = 1
        except:
            referrer = None
            referrer_bonus = 1
        try:
            user_username = user_username.lower()
        except:
            user_username = None
        await adding_data(user_id, user_username, referrer, referrer_bonus,
                          datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    user_channel_status = await bot.get_chat_member(chat_id=channel, user_id=user_id)
    print(user_channel_status)
    user_channel_status = await bot.get_chat_member(chat_id=channel, user_id=user_id)
    a = check_sub_channel(await bot.get_chat_member(chat_id=channel, user_id=message.from_user.id))
    #    b = check_sub_channel(await bot.get_chat_member(chat_id=channel2, user_id=message.from_user.id))
    if a:
        await main_message(user_id)
    else:
        await bot.send_message(message.from_user.id,
                               'Чтобы воспользоваться полным функционалом бота подпишитесь на данные'
                               'каналы и нажмите "Готово"',
                               reply_markup=await update_follow_menu_keyboard(channel))


@router.callback_query(Text('yes'))
async def handler2(callback: CallbackQuery, state: FSMContext):
    print(callback.message.from_user.id)
    #  sent_message = await bot.send_message(callback.message.chat.id, 'Проверяем')
    #  await bot.delete_message(callback.message.from_user.id, callback.message.message_id)
    a = check_sub_channel(await bot.get_chat_member(chat_id=channel, user_id=callback.from_user.id))
    if a:
        await bot.send_message(callback.from_user.id,
                               'Выберите интересующий вас продукт.\n\n Для перезапуска бота нажмите /start',
                               reply_markup=default_kb99)
        await state.set_state(Zaim.state)
    else:
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
        await bot.send_message(callback.from_user.id, 'В доступе отказано. Подпишитесь на все каналы.',
                               reply_markup=inline_kb1)


#      await bot.delete_message(chat_id=callback.message.chat.id, message_id = callback.message.message_id, text = 'В доступе отказано. Подпишитесь на все каналы.', reply_markup=inline_kb1)


@router.message(Text('Привязать карту'))
async def handler20(message: Message, state: FSMContext):
    await message.answer('Введите номер карты')
    await state.set_state(Karta.state2)


@router.message(Karta.state2)
async def handler21(message: Message, state: FSMContext):
    user_id = message.from_user.id
    karta = message.text
    await add_karta(user_id, karta)
    await message.answer('Ваша карта успешно привязана!')
    await state.clear()


@router.message(Text('Изменить номер карты'))
async def handler20(message: Message, state: FSMContext):
    await message.answer('Введите новый номер карты')
    await state.set_state(Karta.state3)


@router.message(Karta.state3)
async def handler21(message: Message, state: FSMContext):
    user_id = message.from_user.id
    karta = message.text
    await add_karta(user_id, karta)
    await message.answer('Новая карта успешно привязана!')
    await state.clear()


if usd_or_rub.lower() == "usd":
    сurrency_sign = "$"
elif usd_or_rub.lower() == "rub":
    сurrency_sign = "₽"


def get_price():
    if currency.upper() == "BTC":
        response = requests.get(
            f"https://api.coingecko.com/api/v3/coins/markets?vs_currency={usd_or_rub}&ids=bitcoin").json()
    elif currency.upper() == "ETH":
        response = requests.get(
            f"https://api.coingecko.com/api/v3/coins/markets?vs_currency={usd_or_rub}&ids=ethereum").json()
    elif currency.upper() == "USDT":
        response = requests.get(
            f"https://api.coingecko.com/api/v3/coins/markets?vs_currency={usd_or_rub}&ids=tether").json()
    elif currency.upper() == "BNB":
        response = requests.get(
            f"https://api.coingecko.com/api/v3/coins/markets?vs_currency={usd_or_rub}&ids=binancecoin").json()
    elif currency.upper() == "SOL":
        response = requests.get(
            f"https://api.coingecko.com/api/v3/coins/markets?vs_currency={usd_or_rub}&ids=solana").json()
    elif currency.upper() == "XRP":
        response = requests.get(
            f"https://api.coingecko.com/api/v3/coins/markets?vs_currency={usd_or_rub}&ids=ripple").json()
    elif currency.upper() == "ADA":
        response = requests.get(
            f"https://api.coingecko.com/api/v3/coins/markets?vs_currency={usd_or_rub}&ids=cardano").json()
    elif currency.upper() == "DOGE":
        response = requests.get(
            f"https://api.coingecko.com/api/v3/coins/markets?vs_currency={usd_or_rub}&ids=dogecoin").json()
    elif currency.upper() == "TON":
        response = requests.get(
            f"https://api.coingecko.com/api/v3/coins/markets?vs_currency={usd_or_rub}&ids=the-open-network").json()
    price = response[0]["current_price"]
    return price


@router.message(Text('Мой аккаунт'))
async def handler41(message: Message):
    user_id = message.from_user.id
    await main_message(user_id)


async def main_message(user_id):
    try:
        referrals = len(await select_user_id_where_referrer_id_and_referrer_bonus_1(user_id))
    except:
        referrals = 0
    karta = await get_kard_number(user_id)
    print(karta)
    if karta[0][0] is not None:
        karta = await get_kard_number(user_id)
        kart_number = karta[0][0]
        await bot.send_message(user_id,
                               "<b>Добро пожаловать на борт!т</b>\n\n"
                               f"<b>Ваша реферальная ссылка:</b>\n"
                               f"<b><code>https://t.me/{(await bot.get_me()).username}?start={user_id}</code></b>\n\n"
                               f"<b>Ваша дата регистрации в боте: <code>{await select_entry_date_where_user_id(user_id)}</code> (По МСК)</b>\n\n"
                               f"<b>Наш <a href='https://t.me/{channel[1:]}'>канал</a> в Телеграмме:</b>\n"
                               f"<b><code>https://t.me/{channel[1:]}</code></b>\n\n"
                               f"<b>У вас <code>{referrals}</code> подтвержденных рефералов</b>\n\n"
                               f"<b>Ваш баланс: <code>{float((Decimal(await select_user_balance_where_user_id(user_id))).quantize(Decimal('1.1000000')))} {currency}</code>   (<code>{float((Decimal(await select_user_balance_where_user_id(user_id)) * Decimal(get_price())).quantize(Decimal('1.10')))}{сurrency_sign}</code>)</b>\n\n"
                               f"<b>Реквизиты карты для вывода: <code>{kart_number}</code></b>",
                               #                          f"<b>Ваш ID: <code>{user_id}</code></b>",
                               reply_markup=default_kb81)
    else:
        await bot.send_message(user_id,
                               "<b>Добро пожаловать на борт!т</b>\n\n"
                               f"<b>Ваша реферальная ссылка:</b>\n"
                               f"<b><code>https://t.me/{(await bot.get_me()).username}?start={user_id}</code></b>\n\n"
                               f"<b>Ваша дата регистрации в боте: <code>{await select_entry_date_where_user_id(user_id)}</code> (По МСК)</b>\n\n"
                               f"<b>Наш <a href='https://t.me/{channel[1:]}'>канал</a> в Телеграмме:</b>\n"
                               f"<b><code>https://t.me/{channel[1:]}</code></b>\n\n"
                               f"<b>У вас <code>{referrals}</code> подтвержденных рефералов</b>\n\n"
                               f"<b>Ваш баланс: <code>{float((Decimal(await select_user_balance_where_user_id(user_id))).quantize(Decimal('1.1000000')))} {currency}</code>   (<code>{float((Decimal(await select_user_balance_where_user_id(user_id)) * Decimal(get_price())).quantize(Decimal('1.10')))}{сurrency_sign}</code>)</b>\n\n",
                               #                          f"<b>Ваш ID: <code>{user_id}</code></b>",
                               reply_markup=default_kb2)


async def no_follow_message(user_id):
    await bot.send_message(user_id,
                           f"<b>Чтобы воспользоваться функционалом бота подпишитесь на <a href='https://t.me/{channel[1:]}'>канал</a> затем нажмите кнопку проверить.</b>\n\n",
                           reply_markup=await update_follow_menu_keyboard(channel))


@router.message(Command("admin"))
async def admin_menu(message: types.Message):
    user_id = message.from_user.id
    await message.delete()
    await bot.send_message(admins_id,
                           "<b>Включено админ меню</b>",
                           reply_markup=default_kb23)


@router.message(Text('Стать партнером!'))
async def start_command(message: types.Message):
    await create_database()
    user_id = message.from_user.id
    user_username = message.from_user.username
    if await select_user_id_where_user_id(user_id) is None:
        try:
            referrer = int(message.text.split()[1])
            if user_id != referrer:
                referrer_bonus = 0
            else:
                referrer = None
                referrer_bonus = 1
        except:
            referrer = None
            referrer_bonus = 1
        try:
            user_username = user_username.lower()
        except:
            user_username = None
        await adding_data(user_id, user_username, referrer, referrer_bonus,
                          datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    user_channel_status = await bot.get_chat_member(chat_id=channel, user_id=user_id)
    print(user_channel_status)
    user_channel_status = await bot.get_chat_member(chat_id=channel, user_id=user_id)
    if user_channel_status.status != "left":
        await main_message(user_id)
    else:
        await no_follow_message(user_id)


### ---___--- ЮЗЕР МЕНЮ ---___--- ###


@router.callback_query(Text("update_balance"))
async def update_balance_call(call: types.CallbackQuery):
    await call.message.delete()
    user_id = call.from_user.id
    user_username = call.from_user.username
    try:
        user_username = user_username.lower()
    except:
        user_username = None
    await changing_username_where_user_id(user_username, user_id)
    user_channel_status = await bot.get_chat_member(chat_id=channel, user_id=user_id)
    if user_channel_status["status"] != "left":
        await main_message(user_id)
    else:
        await no_follow_message(user_id)


@router.message(Text("Вывести"))
async def withdraw_funds_call(message: Message, state: FSMContext):
    user_id = message.from_user.id
    minimal_withdrawal_amount = 0
    if await select_user_balance_where_user_id(user_id) < minimal_withdrawal_amount:
        await bot.answer_callback_query(message.chat.id, text=
        "Недостаточно средств.")
    else:
        await bot.send_message(user_id,
                               "Введите сумму вывода баланса",
                               reply_markup=inline_kb26)
        await state.set_state(withdrawal_of_balance.withdrawal_amount_state)


@router.callback_query(Text("update_follow"))
async def update_follow_call(callback: CallbackQuery):
    await callback.message.delete()
    user_id = callback.from_user.id
    user_username = callback.from_user.username
    user_channel_status = await bot.get_chat_member(chat_id=channel, user_id=user_id)
    if user_channel_status.status != "left":
        await main_message(user_id)
        if await select_referrer_bonus_where_user_id(user_id) == 0:
            await adding_user_balance_where_user_id(await select_referrer_id_where_user_id(user_id))
            await changing_referrer_bonus_where_user_id(1, user_id)
            try:
                await bot.send_message(await select_referrer_id_where_user_id(user_id),
                                       f"<b>У вас новый Реферал ({user_username.lower()}), ваш баланс пополнен на <code>{amount_per_one} {currency}</code></b>\n"
                                       f"<b>Ваш баланс: <code>{float(Decimal(await select_user_balance_where_user_id(await select_referrer_id_where_user_id(user_id))).quantize(Decimal('1.1000000')))} {currency}</code>   ({float(Decimal((Decimal(await select_user_balance_where_user_id(await select_referrer_id_where_user_id(user_id))) * Decimal(get_price()))).quantize(Decimal('1.10')))}{сurrency_sign})</b>",
                                       reply_markup=inline_kb26)
            except:
                await bot.send_message(await select_referrer_id_where_user_id(user_id),
                                       f"<b>У вас новый Реферал ({user_id}), ваш баланс пополнен на <code>{amount_per_one} {currency}</code></b>\n"
                                       f"<b>Ваш баланс: <code>{float(Decimal(await select_user_balance_where_user_id(await select_referrer_id_where_user_id(user_id))).quantize(Decimal('1.1000000')))} {currency}</code>   ({float(Decimal((Decimal(await select_user_balance_where_user_id(await select_referrer_id_where_user_id(user_id))) * Decimal(get_price()))).quantize(Decimal('1.10')))}{сurrency_sign})</b>",
                                       reply_markup=inline_kb26)
    else:
        await no_follow_message(user_id)


@router.message(withdrawal_of_balance.withdrawal_amount_state)
async def withdraw_funds_call(message: Message):
    user_id = message.from_user.id
    karta = await get_kard_number(user_id)
    kard_number = karta[0][0]
    user_username = message.from_user.username
    withdrawal_amount = message.text
    if await select_user_balance_where_user_id(user_id) > float(withdrawal_amount) > minimal_vivod:
        await changing_user_balance_where_user_id(
            (await select_user_balance_where_user_id(user_id) - float(withdrawal_amount)), user_id)
        await message.delete()
        await bot.send_message(user_id,
                               "<b>Заявка на вывод средств:</b>\n"
                               f"<b>Сумма: <code>{withdrawal_amount} {currency}</code></b>\n"
                               f"<b>Ваш ID: {user_id}</b>\n"
                               f"<b>В случае каких либо проблем с выводом необходимо обратиться: {admin_user}</b>\n",
                               reply_markup=inline_kb26)
        await bot.send_message(admins_id,
                               f"<b>Пользователь @{user_username} ({user_id}) хочет вывести {withdrawal_amount} {currency}\n"
                               f"Реквизиты для вывода: {kard_number}</b>",
                               reply_markup=inline_kb26)
    else:
        if float(withdrawal_amount) > await select_user_balance_where_user_id(user_id):
            await message.delete()
            await bot.send_message(user_id,
                                   "Не достаточно средств",
                                   reply_markup=inline_kb26)
        elif minimal_vivod > float(withdrawal_amount):
            await message.delete()
            await bot.send_message(user_id,
                                   f"Минимальная сумма вывода средств: {minimal_vivod}",
                                   reply_markup=inline_kb26)


### ---___--- АДМИН МЕНЮ ---___--- ###


@router.callback_query(Text("number_users"))
async def number_users_admin(call: types.CallbackQuery):
    user_id = call.from_user.id
    await bot.send_message(user_id,
                           f"<b>Всего пользователей</b>: {len(await select_all_user_id())}",
                           reply_markup=inline_kb24)


# @router.callback_query(Text("update_info"))
# async def update_number_users_admin(callback: CallbackQuery):
#    await callback.message.delete()
#    user_id = callback.from_user.id
#    await bot.send_message(user_id,
#                           f"<b>Всего пользователей: {len(await select_all_user_id())}</b>",
#                           reply_markup=await info_menu_keyboard())


@router.callback_query(Text("download_database"))
async def download_database_admin(callback: CallbackQuery):
    user_id = callback.from_user.id
    await bot.send_document(user_id,
                            open("database2.db", "rb"),
                            reply_markup=inline_kb26)


@router.callback_query(Text("private_message"))
async def private_message_admin(call: types.CallbackQuery):
    user_id = call.from_user.id
    await bot.send_message(user_id,
                           "<b>Введите ID пользователя, либо Username</b>",
                           reply_markup=inline_kb26)
    await private_message.id_or_username_state.set()


@router.callback_query(Text("mailing"))
async def send_all_admin(call: types.CallbackQuery):
    user_id = call.from_user.id
    await bot.send_message(user_id,
                           "<b>Введите сообещние для рассылки</b>",
                           reply_markup=inline_kb26)
    await receiving_a_message.receiving_message_state.set()


@router.callback_query(Text("changing_balance"))
async def changing_balance_admin(call: types.CallbackQuery):
    user_id = call.from_user.id
    await bot.send_message(user_id,
                           "<b>Введите ID пользователя, либо Username</b>",
                           reply_markup=inline_kb26)
    await changing_the_balance.id_or_username_state.set()


@router.message(private_message.id_or_username_state)
async def private_message_id_or_username_admin_handler(message: types.Message, state: FSMContext):
    await message.delete()
    username_or_id = message.text
    if username_or_id.isnumeric():
        try:
            if username_or_id == str((await select_user_id_where_user_id(username_or_id))[0]):
                await state.update_data(username_or_id=username_or_id)
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id - 1,
                                            text="<b>Введите сообщение для отправки</b>",
                                            reply_markup=inline_kb26)
                await private_message.private_message_state.set()
        except:
            await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id - 1,
                                        text="<b>Пользователь не найден</b>",
                                        reply_markup=inline_kb26)
            await state.finish()
    else:
        try:
            username_or_id = username_or_id.replace("@", "").lower()
            if username_or_id == str(await select_user_username_where_user_name(username_or_id)):
                await state.update_data(username_or_id=username_or_id)
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id - 1,
                                            text="<b>Введит е сообщение для отправки</b>",
                                            reply_markup=inline_kb26)
                await private_message.private_message_state.set()
        except:
            await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id - 1,
                                        text="<b>Пользователь не найден</b>",
                                        reply_markup=inline_kb26)
            await state.finish()


@router.message(private_message.private_message_state)
async def private_message_private_message_admin_handler(message: types.Message, state: FSMContext):
    private_message_text = message.text
    await message.delete()
    data = await state.get_data()
    username_or_id = data.get("username_or_id")
    if username_or_id.isnumeric():
        await bot.send_message(username_or_id,
                               private_message_text,
                               reply_markup=inline_kb26)
    else:
        username_or_id = await select_user_id_where_user_username(username_or_id)
        await bot.send_message(username_or_id,
                               private_message_text,
                               reply_markup=inline_kb26)

    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id - 2,
                                text=f"<b>Пользователю {username_or_id} отправили сообщение {private_message_text}</b>",
                                reply_markup=inline_kb26)
    await state.finish()


@router.message(receiving_a_message.receiving_message_state)
async def receiving_a_message_receiving_message_admin_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text
    await state.finish()
    await message.delete()
    for users in await select_all_user_id():
        try:
            await bot.send_message(chat_id=users[0], text=text,
                                   reply_markup=inline_kb26)
        except:
            pass
    await bot.send_message(user_id, "<b>Массовая рассылка успешно завершена!</b>",
                           reply_markup=inline_kb26)


@router.message(changing_the_balance.id_or_username_state)
async def changing_the_balance_id_or_username_admin_handler(message: types.Message, state: FSMContext):
    username_or_id = message.text
    await message.delete()
    username_or_id = username_or_id.replace("@", "").lower()
    if username_or_id.isnumeric():
        try:
            if username_or_id == str((await select_user_id_where_user_id(username_or_id))[0]):
                await state.update_data(username_or_id=username_or_id)
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id - 1,
                                            text="<b>Введите число на какое изменить баланс</b>",
                                            reply_markup=inline_kb26)
                await changing_the_balance.change_amount_state.set()
        except:
            await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id - 1,
                                        text="<b>Пользователь не найден</b>",
                                        reply_markup=inline_kb26)
            await state.finish()
    else:
        try:
            if username_or_id == str(await select_user_username_where_user_name(username_or_id)):
                await state.update_data(username_or_id=username_or_id)
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id - 1,
                                            text="<b>Введите число на какое изменить баланс</b>",
                                            reply_markup=inline_kb26)
                await changing_the_balance.change_amount_state.set()
        except:
            await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id - 1,
                                        text="<b>Пользователь не найден</b>",
                                        reply_markup=inline_kb26)
            await state.finish()


@router.message(changing_the_balance.change_amount_state)
async def changing_the_balance_change_amount_admin_handler(message: types.Message, state: FSMContext):
    change_amount_state = message.text
    await message.delete()
    await state.update_data(change_amount=change_amount_state)
    data = await state.get_data()
    username_or_id = data.get("username_or_id")
    change_amount_state = data.get("change_amount")
    if username_or_id.isnumeric():
        await changing_user_balance_where_user_id(change_amount_state, username_or_id)
    else:
        await changing_user_balance_where_user_username(change_amount_state, username_or_id)
    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id - 2,
                                text=f"<b>У пользователя {username_or_id} баланс {change_amount_state}</b>",
                                reply_markup=inline_kb26)
    await state.finish()


@router.callback_query(Text("deleted_message"))
async def deleted_message_call(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.delete()
