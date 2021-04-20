from pyrogram import Client as Bot

from callsmusic import run
from Mizuki import API_ID, API_HASH, TOKEN


bot = Bot(
    ":memory:",
    API_ID,
    API_HASH,
    token=TOKEN,
    plugins=dict(root="handlers")
)

bot.start()
run()
