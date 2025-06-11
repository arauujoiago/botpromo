from telethon import TelegramClient, events
from telethon.sessions import StringSession
import os

api_id = int(os.environ.get('API_ID'))
api_hash = os.environ.get('API_HASH')
session_string = os.environ.get('SESSION_STRING')

client = TelegramClient(StringSession(session_string), api_id, api_hash)

keywords = ['a56', 'sabão', 'a36', '14s', 'poco x7']

@client.on(events.NewMessage)
async def handler(event):
    message = event.message.message.lower()
    if any(keyword in message for keyword in keywords):
        await client.send_message('me', f"🔔 Palavra-chave detectada: {message}")

print("Bot rodando...")
client.start()
client.run_until_disconnected()
