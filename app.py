import os
import threading
from flask import Flask, request, jsonify, send_from_directory
import discord
from discord.ext import commands

# Initialize Flask and Bot
app = Flask(__name__, static_folder='.')
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Configuration
TOKEN = os.environ.get('DISCORD_TOKEN')
MY_USER_ID = 715160948675182613

@app.route('/')
def index():
    return send_from_directory('.', 'date.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    # Schedule the coroutine to run in the bot's event loop
    bot.loop.create_task(send_dm(data.get('activity'), data.get('date'), data.get('notes')))
    return jsonify({"status": "success"}), 200

async def send_dm(activity, date, notes):
    try:
        user = await bot.fetch_user(MY_USER_ID)
        await user.send(f"📅 **New Date:** {activity}\nDate: {date}\nNotes: {notes}")
    except Exception as e:
        print(f"DM Error: {e}")

# Run the bot in a separate thread
def run_bot():
    bot.run(TOKEN)

if __name__ == '__main__':
    threading.Thread(target=run_bot, daemon=True).start()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
