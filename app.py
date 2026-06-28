import os
import threading
from flask import Flask, request, jsonify, send_from_directory
import discord
from discord.ext import commands

app = Flask(__name__, static_folder='.')

# Load variables from Railway
TOKEN = os.environ.get('DISCORD-TOKEN')
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
    print(f"DEBUG: Data received: {data}")
    activity = data.get('activity')
    date = data.get('date')
    notes = data.get('notes', 'No notes provided')
    
    # Send the DM
    bot.loop.create_task(send_dm(activity, date, notes))
    return jsonify({"status": "success"}), 200

async def send_dm(activity, date, notes):
    try:
        user = await bot.fetch_user(MY_USER_ID)
        await user.send(f"📅 **New Date!**\nActivity: {activity}\nDate: {date}\nNotes: {notes}")
    except Exception as e:
        print(f"DM ERROR: {e}")

# Start the Bot in a background thread
def run_bot():
    bot.run(TOKEN)

if __name__ == '__main__':
    threading.Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
