from aiogram.dispatcher.filters.state import StatesGroup, State


class States(StatesGroup):
    choose_type_app = State()
    choose_username = State()
    choose_cabinet = State()
    choose_device = State()
    choose_problem_text = State()
    finish_state = State()
