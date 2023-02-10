from aiogram import types
import game
import bot
import text


async def player_turn(message: types.Message):
    name = message.from_user.full_name
    await message.answer(f'{name}, твой ход! Сколько конфет возьмешь?')


async def player_game(message: types.Message, take: str, name: str):
    if take.isdigit():
        take = int(take)
        if (game.get_total() - take) < 0:
            await message.answer(f'{name}, хочет взять - {take} {text.declension_sweets(take)[0]},'
                                 f' но на столе всего {game.get_total()}.\n'
                                 f'Придётся взять меньше.')
        elif take <= 0 or take > 28:
            await message.answer(f'{name}, можно брать не менее 1 и '
                                 f'не более 28!')
        elif 1 <= take <= 28:
            game.take_sweets(take)
            if await game.check_win(message, 'player', take):
                return
            await message.answer(f'{name} берет {take} {text.declension_sweets(take)[0]}.'
                                    f'\nНа столе осталось {game.get_total()} '
                                    f'{text.declension_sweets(game.get_total())[1]}. Ходит бот!')
            await bot.bot_turn(message)
    else:
        await message.answer(f'Что-то не так. Ты точно написал число?')