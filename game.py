from aiogram import types
import text

set_total = 150
total = set_total
game = False
level = 'с глупым ботом'


def update_total():
    global total
    global set_total
    total = set_total


def set_total_sweets(value: int):
    global set_total
    set_total = value
    return set_total


def get_total():
    global total
    return total


def take_sweets(take: int):
    global total
    total -= take
    return total


def new_game():
    global game
    global total
    if game:
        game = False
    else:
        game = True
        total = set_total
    return game


def check_game():
    global game
    return game


async def check_win(message: types.Message, player: str, take: int):
    name = message.from_user.full_name
    global game
    global level
    if get_total() == 0:
        if player == 'player':
            await message.answer(f'{name} берет {take} {text.declension_sweets(take)[0]}. '
                                 f'\nВот и кончились конфеты! '
                                 f'\nВыиграл(-а) {name}!'
                                 f'\n\nСыграть заново -> /new_game или /игра'
                                 f'\nВыйти в меню -> /menu или /меню')

        else:
            await message.answer(f'Конфет больше нет! Я выиграл!\n'
                                 f'\n\nСыграть заново -> /new_game или /игра'
                                 f'\nВыйти в меню -> /menu или /меню')
        new_game()
        return True
    else:
        return False


def change_level():
    global level
    if level == 'с глупым ботом':
        level = 'с умным ботом'
    else:
        level = 'с глупым ботом'
    return level