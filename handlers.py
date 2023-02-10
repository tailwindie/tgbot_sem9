import random

from aiogram import types

import bot
import game
import player
from create import dp
import text


@dp.message_handler(commands=['start', 'старт'])
async def start(message: types.Message):
    name = message.from_user.full_name
    await message.answer(f'{name}{text.greetings}')


@dp.message_handler(commands=['rules', 'правила'])
async def game_rules(message: types.Message):
    """Правила игры"""
    name = message.from_user.full_name
    await message.answer(f'{name}{text.rules}')


@dp.message_handler(commands=['new_game', 'игра'])
async def new_game(message: types.Message):
    """Запуск игры"""
    if not game.check_game():
        game.new_game()
    else:
        game.update_total()
    name = message.from_user.full_name
    if game.check_game():
        await message.answer(f'{name}, на столе лежит {game.get_total()} '
                             f'{(text.declension_sweets(game.get_total()))[1]}.\nСтартуем!')
        turn = random.choice([True, False])
        if turn:
            await player.player_turn(message)
        else:
            await message.answer(f'{name}, я хожу первым!')
            await bot.bot_turn(message)


@dp.message_handler(commands=['set_total', 'хочу'])
async def set_total(message: types.Message):
    if not game.check_game():
        total = message.text.split()
        if len(total) > 1 and total[1].isdigit():
            game.set_total_sweets(int(total[1]))
            await message.answer(f'Kоличество конфет изменено на {total[1]}'
                                 f'\nНачать игру -> /new_game или /игра'
                                 f'\nВыйти в меню -> /menu или /меню')
        else:
            await message.answer(text.answer1_for_set_total)
    else:
        await message.answer(text.answer2_for_set_total)


@dp.message_handler(commands=['level', 'уровень'])
async def game_level(message: types.Message):
    if not game.check_game():
        level = game.change_level()
        await message.answer(f'Ты будешь играть {level}.'
                             f'\nЧтобы поменять уровень сложности, еще раз используй эту же команду.')
    else:
        await message.answer(text.answer_for_level)


@dp.message_handler(commands=['menu', 'меню'])
async def show_menu(message: types.Message):
    name = message.from_user.full_name
    await message.answer(f'{name}{text.menu}')


@dp.message_handler(commands=['stop', 'стоп'])
async def stop_game(message: types.Message):
    game.new_game()
    await message.answer(text.stop_game)


@dp.message_handler()
async def game_sweets(message: types.Message):
    name = message.from_user.full_name
    take = message.text
    if game.check_game():
        await player.player_game(message, take, name)
    else:
        await message.answer(f'{name}{text.menu}')