from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

button_2 = [
    [
        InlineKeyboardButton(text='Подписаться', url='https://t.me/ttttxtxer')
    ],
    [
        InlineKeyboardButton(text='Подписался', callback_data='yes')
    ]
]
inline_kb1 = InlineKeyboardMarkup(inline_keyboard=button_2)

button4 = [
    [
        KeyboardButton(text='Привязать карту')
        #    KeyboardButton(text='Вывести')
    ]
]
default_kb2 = ReplyKeyboardMarkup(keyboard=button4, resize_keyboard=True)

button81 = [
    [
        KeyboardButton(text='Мой аккаунт'),
        KeyboardButton(text='Изменить номер карты')
    ],
    [
        KeyboardButton(text='Вывести')
    ]
]
default_kb81 = ReplyKeyboardMarkup(keyboard=button81, resize_keyboard=True)

button4 = [
    [
        KeyboardButton(text='Изменить номер карты'),
        KeyboardButton(text='Вывести')
    ]
]
default_kb9 = ReplyKeyboardMarkup(keyboard=button4, resize_keyboard=True)

button043 = [
    [
        InlineKeyboardButton(text="🔄 Обновить баланс", callback_data="update_balance")
    ]
]
inline_kb991 = InlineKeyboardMarkup(inline_keyboard=button043)

button99 = [
    [
        KeyboardButton(text='Стать партнером!')
    ]
]
default_kb99 = ReplyKeyboardMarkup(keyboard=button99, resize_keyboard=True)

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

button5 = [
    [
        #       InlineKeyboardButton(text="Пригласить", switch_inline_query=""),
        #      InlineKeyboardButton(text="Привязать карту", callback_data="update_balance")
        InlineKeyboardButton(text="📥 Вывод средств", callback_data="withdraw_funds")
    ]
]
inline_kb2 = InlineKeyboardMarkup(inline_keyboard=button5, resize_keyboard=True)


async def update_follow_menu_keyboard(channel):
    keyboard = []
    update_follow = InlineKeyboardButton(text="Проверить", callback_data="update_follow")
    channel_link = InlineKeyboardButton(text=" Перейти на канал", url=f"https://t.me/{channel.replace('@', '')}")
    keyboard.append([update_follow, channel_link])
    inline_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return inline_markup



button6 = [
    [
        InlineKeyboardButton(text="👥 Количество пользователей", callback_data="number_users"),
        InlineKeyboardButton(text="⏬ Скачать базу данных", callback_data="download_database"),
        InlineKeyboardButton(text="✉ Личное сообщение", callback_data="private_message")
    ],
    [
        InlineKeyboardButton(text="📪 Массовая рассылка", callback_data="mailing"),
        InlineKeyboardButton(text="💰 Изменение баланса", callback_data="changing_balance"),
        InlineKeyboardButton(text="❌ Закрыть сообщение", callback_data="deleted_message")
    ]
]
default_kb23 = InlineKeyboardMarkup(inline_keyboard=button6)


button25 = [
    [
        #    InlineKeyboardButton(text="🔄 Обновить", callback_data="update_info"),
        InlineKeyboardButton(text="❌ Закрыть сообщение", callback_data="deleted_message")
    ]
]
inline_kb24 = InlineKeyboardMarkup(inline_keyboard=button25)


button32 = [
    [
        InlineKeyboardButton(text="❌ Закрыть сообщение", callback_data="deleted_message")
    ]
]
inline_kb26 = InlineKeyboardMarkup(inline_keyboard=button32)
