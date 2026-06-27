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

# This serves your date.html automatically when you visit the URL
@app.route('/')
def index():
    return send_from_directory('.', 'date.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    bot.loop.create_task(send_dm(data.get('activity'), data.get('date')))
    return jsonify({"status": "received"}), 200

async def send_dm(activity, date):
    user = await bot.fetch_user(MY_USER_ID)
    await user.send(f"📅 **Date Idea:** {activity} on {date}")

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

@bot.event
async def on_ready():
    print(f'Bot is ready!')

if __name__ == '__main__':
    threading.Thread(target=run_flask).start()
    bot.run(TOKEN)
