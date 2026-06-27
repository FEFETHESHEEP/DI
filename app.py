import os
import threading
from flask import Flask, request, jsonify
import discord
from discord.ext import commands

app = Flask(__name__)
TOKEN = os.environ.get('DISCORD_TOKEN')
MY_USER_ID = 715160948675182613 

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@app.route('/', methods=['GET'])
def home():
    return "Bot is online!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    activity = data.get('activity')
    date = data.get('date')
    bot.loop.create_task(send_dm(activity, date))
    return jsonify({"status": "received"}), 200

async def send_dm(activity, date):
    user = await bot.fetch_user(MY_USER_ID)
    await user.send(f"📅 **Date Idea:** {activity} on {date}")

if __name__ == '__main__':
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=5000)).start()
    bot.run(TOKEN)
