from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile

import bot_cmd
import keyboards as kb
import database as db
from dotenv import load_dotenv
import os

import pay_yookassa
from word.temp_word import read_doc

# from bot_cmd import private
# import asyncio
# ALLOWED_UPDATES = ['message, edited_message']

storage = MemoryStorage()
load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot=bot, storage=storage)


async def on_startup(_):
    global list_param
    list_param = read_doc()
    await db.start_db(list_param)
    print('Бот успешно запущен!')


class NewOrder(StatesGroup):
    admin = State()
    start_calc = State()
    param1 = State()
    param2 = State()
    param3 = State()
    param4 = State()
    pay = State()
    restart = State()


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    # await db.cmd_start_db(message.from_user.id)
    await message.answer_sticker('CAACAgIAAxkBAAMpZBAAAfUO9xqQuhom1S8wBMW98ausAAI4CwACTuSZSzKxR9LZT4zQLwQ')
    await message.answer(f'{message.from_user.first_name}, добро пожаловать в службу какого-то расчета!')
    # print(message.from_user.id)

    # ADMIN_ID = 177378414
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer('Вы авторизовались как администратор!',
                             reply_markup=kb.main_admin)
        await NewOrder.admin.set()

    else:
        await db.write_user_db(id_user=message.from_user.id,
                            first_name=message.from_user.first_name)
        await message.answer(f'Начните расчет!', reply_markup=kb.main)
        await NewOrder.start_calc.set()

@dp.message_handler(commands=['reset'])
async def recalc(message: types.Message):
    await message.answer('Новый расчет!', reply_markup=kb.main)
    await NewOrder.param1.set()
    await message.answer(f'Введите числовое значение параметра "{list_param[0]}"')


@dp.message_handler(commands='question')
async def question_admin(message, keybord=None):
    await bot.send_message(chat_id=int(os.getenv('ADMIN_ID')),
                           text=f'Вопрос администратору от {message.from_user.first_name}!')
    await message.answer(f'С вами свяжется администратор', reply_markup=keybord)


@dp.message_handler(state=NewOrder.start_calc)
async def calc_start(message: types.Message):
    if message.text == 'Начать расчет':
        await NewOrder.param1.set()
        await message.answer(f'Введите числовое значение параметра "{list_param[0]}"')
                             # reply_markup=kb.user_panel)
    else:
        if message.text == '/question':
            await question_admin(message)
        else:
            await message.answer(f'Начните расчет!', reply_markup=kb.main)

@dp.message_handler(state=NewOrder.param1)
async def get_param1(message: types.Message):
    try:
        param = float(message.text)
        await db.write_parametr_db(id_user=message.from_user.id,
                                                id_parametr=0,
                                                content=param)
        await NewOrder.param2.set()
        await message.answer(f'Введите числовое значение параметра "{list_param[2]}"')
                             # reply_markup=kb.user_panel)
    except:
        if message.text == '/question':
            await question_admin(message)
        else:
            await message.answer(
                f'Недопустимый формат данных.\nВведите числовое значение параметра "{list_param[0]}"')
                # reply_markup=kb.user_panel)

@dp.message_handler(state=NewOrder.param2)
async def get_param2(message: types.Message):
    try:
        param = float(message.text)
        await db.write_parametr_db(id_user=message.from_user.id,
                                                id_parametr=2,
                                                content=param)
        await NewOrder.param3.set()
        await message.answer(f'Введите числовое значение параметра "{list_param[3]}"')
                             # reply_markup=kb.user_panel)
    except:
        if message.text == '/question':
            await question_admin(message)
        else:
            await message.answer(
                f'Недопустимый формат данных.\nВведите числовое значение параметра "{list_param[2]}"')
                # reply_markup=kb.user_panel)

@dp.message_handler(state=NewOrder.param3)
async def get_param3(message: types.Message):
    try:
        param = float(message.text)
        await db.write_parametr_db(id_user=message.from_user.id,
                                                id_parametr=3,
                                                content=param)
        await NewOrder.param4.set()
        await message.answer(f'Введите числовое значение параметра "{list_param[5]}"')
                             # reply_markup=kb.user_panel)
    except:
        if message.text == '/question':
            await question_admin(message)
        else:
            await message.answer(
                f'Недопустимый формат данных.\nВведите числовое значение параметра "{list_param[3]}"')
                # reply_markup=kb.user_panel)

@dp.message_handler(state=NewOrder.param4)
async def get_param4_end(message: types.Message):
    try:
        param = float(message.text)
        await db.write_parametr_db(id_user=message.from_user.id,
                                                id_parametr=5,
                                                content=param)
        await message.answer('Расчет закончен, для его получения необходимо произвести оплату',
                             reply_markup=kb.user_pay)
        await NewOrder.pay.set()
        # await bot.send_message(int(os.getenv('ADMIN_ID')), message.from_user.id)
    except:
        if message.text == '/question':
            await question_admin(message)
        else:
            await message.answer(
                f'Недопустимый формат данных.\nВведите числовое значение параметра "{list_param[5]}"')
                # reply_markup=kb.user_panel)

@dp.message_handler(state=NewOrder.pay)
async def pay(message: types.Message):
    if message.text == 'Оплатить':
        await message.answer('Ожидание оплаты...')
        number_pay, summa = pay_yookassa.test_pay()
        await db.write_pay_db(id_user=message.from_user.id, id_pay=number_pay)
        await db.read_calc_write(id_user=message.from_user.id, list_param=list_param)
        await message.answer('Оплата прошла', reply_markup=kb.user_recalc)
        await message.answer_document(InputFile('файл расчета.docx'))
        os.remove('файл расчета.docx')
        await bot.send_message(chat_id=int(os.getenv('ADMIN_ID')),
                               text=f"Пользователь {message.from_user.first_name} совершил оплату.\n"
                                    f" Квитанция № {number_pay} на сумму {summa} рублей")
        await NewOrder.restart.set()
    else:
        if message.text == '/question':
            await question_admin(message, kb.user_pay)
        else:
            await message.answer('Нажмите кнопку оплатить', reply_markup=kb.user_pay)

@dp.message_handler(text='Загрузить файл повторно',state=NewOrder.restart)
async def load_file(message: types.Message):
    await db.read_calc_write(id_user=message.from_user.id, list_param=list_param)
    await message.answer_document(InputFile('файл расчета.docx'))
    os.remove('файл расчета.docx')


@dp.message_handler()
async def answer(message: types.Message):
    await message.reply('Данное сообщение не определено.')



if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)




#
#
# if __name__ == '__main__':
#     async def main():
#         await bot.delete_webhook(drop_pending_updates=True)
#         # await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats)
#         await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
#         await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)
#     asyncio.run(main())
#
# # executor.start_polling(dp, skip_updates=True)
#
#

