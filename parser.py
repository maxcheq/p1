import asyncio
from telethon import TelegramClient, errors
from datetime import datetime
import socket

# Ваши данные
api_id = '11306461'
api_hash = 'edb894d685ab387841e9fe7600fd2a94'
phone_number = '+27 74 432 2007'

message_text = """🐺 HUSKY FLAVORS MENU 🐺
⚡️ 30ML - 50MG ⚡️

✅ Gum Wolf 🐺🍬
✅ Jungle Hunter 🌴🦁
✅ Lemon Flock 🍋🦜
✅ Red Warg 🍒🐺
✅ Shake Pears 🍐✨
✅ Sour Beast 🍋🐉
✅ Tropic Hunter 🥭🍍
✅ Berserk 🪓🐺
✅ Sweet Bunchshot 🍭🍬
✅ Yogi Doggi 🐶🍫
✅ Milk River 🥛🏞️
✅ Juicy Madness 🍓🥭
✅ Winter River ❄️🌊
✅ Tropical Dew 🥥🍹
✅ Pink Lemonade 🍋🌸

💰 PRICE: 10€ 💰

📍 Available Locations: Imanta, Zolitude, Agenskalns, Ziepniekkalns, Centrs, Purvciems 
📦 Delivery with OMNIVA - Free for orders of 3 cans or more 📦

➡️ ORDER: @puffterminalriga

Tags
хаски haski hasky huski
juice juicy жижа жижка
zhiza zhizka 50мг 50mg
30ml 30мл вейп vape """

last_sent_info = {}

def is_connected():
    """
    Проверяет, есть ли доступ в интернет.
    """
    try:
        socket.create_connection(("1.1.1.1", 53), timeout=5)
        return True
    except OSError:
        return False

async def send_message_to_group(group):
    group_id = group.id
    now = datetime.now()

    try:
        messages = []
        async for message in client.iter_messages(group, limit=10):
            messages.append(message)

        if group_id in last_sent_info:
            last_info = last_sent_info[group_id]
            our_last_message_id = last_info["last_message_id"]
            our_last_text = last_info["last_text"]

            new_messages = [
                msg for msg in messages
                if msg.id > our_last_message_id and msg.sender_id != (await client.get_me()).id
            ]

            if len(new_messages) < 2:
                print(f"[{now}] В группе {group.title} недостаточно новых сообщений для отправки.")
                return

            for msg in messages:
                if msg.text == message_text:
                    print(f"[{now}] В группе {group.title} найдено сообщение с таким же текстом. Пропускаем.")
                    return

        sent_message = await client.send_message(group, message_text)
        print(f"[{now}] Сообщение отправлено в группу: {group.title}")

        last_sent_info[group_id] = {
            "last_message_id": sent_message.id,
            "last_text": sent_message.text
        }

    except errors.FloodWaitError as e:
        print(f"[{now}] Telegram ограничил действия. Ожидаем {e.seconds} секунд...")
        await asyncio.sleep(e.seconds)
    except Exception as e:
        print(f"[{now}] Ошибка при обработке группы {group.title}: {e}")

async def monitor_groups():
    while True:
        if not is_connected():
            print(f"[{datetime.now()}] Интернет отсутствует. Ожидание подключения...")
            await asyncio.sleep(5)
            continue

        try:
            await client.start(phone=phone_number)
            print(f"[{datetime.now()}] Успешно авторизовались в Telegram.")

            dialogs = await client.get_dialogs()
            groups = [dialog.entity for dialog in dialogs if dialog.is_group]

            for group in groups:
                await send_message_to_group(group)

            print(f"[{datetime.now()}] Завершена проверка всех групп. Ожидание 60 секунд...")
            await asyncio.sleep(60)

        except (errors.ConnectionError, OSError):
            print(f"[{datetime.now()}] Потеряно соединение с интернетом. Переподключение...")
            await asyncio.sleep(5)
        except Exception as e:
            print(f"[{datetime.now()}] Неизвестная ошибка: {e}")
            await asyncio.sleep(10)

if __name__ == '__main__':
    client = TelegramClient('session', api_id, api_hash)
    asyncio.run(monitor_groups())



