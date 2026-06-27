import os
import threading
from flask import Flask, request, jsonify
import discord
from discord.ext import commands

app = Flask(__name__)

# Railway will provide the Token via Environment Variables
TOKEN = os.environ.get('DISCORD_TOKEN')
MY_USER_ID = 715160948675182613 

intents = discord.Intents.default()
intents.message_content = True
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
    # Railway sets the PORT automatically
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

if __name__ == '__main__':
    threading.Thread(target=run_flask).start()
    bot.run(TOKEN)
