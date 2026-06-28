import os
import threading
from flask import Flask, request, jsonify, send_from_directory
import discord
from discord.ext import commands

app = Flask(__name__, static_folder='.')
TOKEN = os.environ.get('DISCORD_TOKEN')
MY_USER_ID = 715160948675182613

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@app.route('/')
def index():
    return send_from_directory('.', 'date.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print(f"Data received: {data}")
    bot.loop.create_task(send_dm(data))
    return jsonify({"status": "success"}), 200

async def send_dm(data):
    try:
        user = await bot.fetch_user(MY_USER_ID)
        await user.send(f"📅 **Date:** {data.get('activity')}\nDate: {data.get('date')}\nNotes: {data.get('notes')}")
    except Exception as e:
        print(f"DM Error: {e}")

if __name__ == '__main__':
    threading.Thread(target=lambda: bot.run(TOKEN)).start()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
