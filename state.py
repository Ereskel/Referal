from aiogram.fsm.state import StatesGroup, State


class Karta(StatesGroup):
    state = State()
    state2 = State()
    state3 = State()


class Zaim(StatesGroup):
    state = State()

