from aiogram.fsm.state import StatesGroup, State
# к опросу
class StepsForm(StatesGroup):
    GET_NAME = State()
    GET_LAST_NAME = State()
    GET_AGE = State()