import threading
from flask import Flask, request, jsonify
import discord
from discord.ext import commands
import os

# 1. Paste your NEW Bot Token here
TOKEN = os.environ.get('DISCORD_TOKEN')# 2. Your user ID
MY_USER_ID = 715160948675182613 

app = Flask(__name__)
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    activity = data.get('activity')
    date = data.get('date')
    bot.loop.create_task(send_dm(activity, date))
    return jsonify({"status": "received"}), 200

async def send_dm(activity, date):
    try:
        user = await bot.fetch_user(MY_USER_ID)
        await user.send(f"📅 **New Date Proposal!**\nActivity: {activity}\nDate: {date}")
    except Exception as e:
        print(f"Error: {e}")

def run_flask():
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    threading.Thread(target=run_flask).start()
    bot.run(TOKEN)
