from telethon import TelegramClient, events
from telethon.sessions import StringSession
from flask import Flask
import os
import threading

# Telegram API info
api_id = int(os.environ.get('API_ID'))
api_hash = os.environ.get('API_HASH')
session_string = os.environ.get('SESSION_STRING')

client = TelegramClient(StringSession(session_string), api_id, api_hash)

# Lista de palavras-chave
keywords = ['a56', 'sabão', 'a36', '14s', 'poco x7']

@client.on(events.NewMessage)
async def handler(event):
    message = event.message.message.lower()
    if any(keyword in message for keyword in keywords):
        await client.send_message('me', f"🔔 Palavra-chave detectada: {event.message.message}")

def start_telegram():
    with client:
        print("Telegram client rodando...")
        client.run_until_disconnected()

# Mini servidor web para evitar que o Render mate o container
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot Telegram rodando no Render!"

# Rodar o Telegram client em uma thread separada
threading.Thread(target=start_telegram).start()

# Iniciar o Flask (para o Render aceitar como Web Service)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
