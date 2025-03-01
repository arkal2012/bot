import os
import telebot
from dotenv import load_dotenv
import time

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# Словарь для хранения данных сессий для каждого чата
session_data = {}

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    text = message.text

    # Если сессия еще не началась, начинаем её с первого сообщения пользователя
    if chat_id not in session_data:
        session_data[chat_id] = {
            "messages": [message.message_id],  # сохраняем ID первого сообщения
            "answers": [text]                  # сохраняем первый ответ
        }
        # Отправляем первый вопрос
        sent = bot.send_message(chat_id, "Введите дату")
        session_data[chat_id]["messages"].append(sent.message_id)
        return

    # Если сессия уже началась, сохраняем сообщение и добавляем его ID
    session_data[chat_id]["answers"].append(text)
    session_data[chat_id]["messages"].append(message.message_id)

    count = len(session_data[chat_id]["answers"])

    if count == 2:
        sent = bot.send_message(chat_id, "Какая ситуация произошла?")
        session_data[chat_id]["messages"].append(sent.message_id)
    elif count == 3:
        sent = bot.send_message(chat_id, "Какие мысли у вас возникли?")
        session_data[chat_id]["messages"].append(sent.message_id)
    elif count == 4:
        sent = bot.send_message(chat_id, "Какая эмоция у вас возникла? Насколько сильная (в %)?")
        session_data[chat_id]["messages"].append(sent.message_id)
        # Отправляем изображение
        try:
            with open('54.jpg', 'rb') as photo:
                photo_msg = bot.send_photo(chat_id, photo)
                session_data[chat_id]["messages"].append(photo_msg.message_id)
        except Exception as e:
            print("Ошибка отправки фото:", e)
    elif count == 5:
        sent = bot.send_message(chat_id, "Какая реакция в теле за этим последовала?")
        session_data[chat_id]["messages"].append(sent.message_id)
    elif count == 6:
        sent = bot.send_message(chat_id, "Какое поведение за этим последовало?")
        session_data[chat_id]["messages"].append(sent.message_id)
    elif count == 7:
        # Сессия завершена – формируем итоговое сообщение
        summary = (
            "\U0001F4CB *Ваши ответы:*\n\n"
            f"\U0001F4C5 Дата: {session_data[chat_id]['answers'][1]}\n"
            f"\U0001F4CC Ситуация: {session_data[chat_id]['answers'][2]}\n"
            f"\U0001F4AD Мысли: {session_data[chat_id]['answers'][3]}\n"
            f"\U0001F614 Эмоция: {session_data[chat_id]['answers'][4]}\n"
            f"\U0001F915 Реакция в теле: {session_data[chat_id]['answers'][5]}\n"
            f"\U0001F6B6 Поведение: {session_data[chat_id]['answers'][6]}"
        )
        final_msg = bot.send_message(chat_id, summary, parse_mode="Markdown")
        session_data[chat_id]["final_id"] = final_msg.message_id

        # Удаляем все сообщения, кроме финального
        for msg_id in session_data[chat_id]["messages"]:
            if msg_id != session_data[chat_id]["final_id"]:
                try:
                    bot.delete_message(chat_id, msg_id)
                except Exception:
                    pass

        # Очищаем данные сессии
        del session_data[chat_id]

# Основной процесс бота
def run_bot():
    while True:
        try:
            bot.remove_webhook()
            bot.polling(none_stop=True, interval=1, timeout=10, long_polling_timeout=20)
        except Exception as e:
            print(f"Произошла ошибка: {e}. Попытка перезапуска через 5 секунд...")
            time.sleep(5)

if __name__ == "__main__":
    run_bot()
