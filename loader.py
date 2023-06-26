from aiogram import Router, Dispatcher, Bot
from config import token

dp = Dispatcher()
bot = Bot(token, parse_mode='HTML')
router = Router()
