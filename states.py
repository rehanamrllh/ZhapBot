from aiogram.fsm.state import State, StatesGroup

class ConvertPDFStates(StatesGroup):
    waiting_for_file = State()
