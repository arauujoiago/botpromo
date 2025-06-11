from telethon import TelegramClient, events
from telethon.sessions import StringSession
from flask import Flask
import os
import asyncio

api_id = int(os.environ.get('API_ID'))
api_hash = os.environ.get('API_HASH')
session_string = os.environ.get('SESSION_STRING')

client = TelegramClient(StringSession(session_string), api_id, api_hash)

keywords = ['a56', 'sabão', 'a36', '14s', 'poco x7']

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot Telegram rodando no Render com Flask!"

@client.on(events.NewMessage)
async def handler(event):
    message_text = event.message.message or ''
    lower_text = message_text.lower()

    if any(keyword in lower_text for keyword in keywords):
        sender = await event.get_sender()
        sender_name = getattr(sender, 'username', 'Desconhecido')

        msg_to_send = f"🔔 Mensagem detectada de @{sender_name}:\n\n{message_text}"

        if event.message.media:
            file_path = await event.message.download_media(file='./downloads/')
            await client.send_message('me', msg_to_send)
            await client.send_file('me', file_path, caption="📎 Mídia detectada.")
            os.remove(file_path)
        else:
            await client.send_message('me', msg_to_send)

async def start_telegram():
    os.makedirs('./downloads/', exist_ok=True)
    await client.start()
    print("Bot Telegram iniciado!")
    await client.run_until_disconnected()

def run():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(start_telegram())  # Inicia o TelegramClient no mesmo loop
    run()  # Roda o Flask (que também usa o mesmo loop)
