from os import path

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

import converter
from callsmusic import callsmusic, queues
from config import DURATION_LIMIT
from downloaders import youtube
from helpers.decorators import authorized_users_only, errors
from helpers.errors import DurationLimitError
from helpers.filters import command, other_filters
from helpers.gets import get_file_name, get_url
from Mizuki.events import Client


@Client.on_message(command(["play", "p"]) & other_filters)
@errors
@authorized_users_only
async def play(_, message: Message):

    lel = await message.reply("🌈 **Sedang Memprosess**...")
    message.from_user.id
    message.from_user.first_name

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="join me if you're sad", url="https://t.me/hbreakclub"
                )
            ]
        ]
    )

    audio = (
        (message.reply_to_message.audio or message.reply_to_message.voice)
        if message.reply_to_message
        else None
    )
    url = get_url(message)

    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"‼️ Video dengan durasi lebih dari {DURATION_LIMIT} menit tidak diperbolehkan untuk diputar!"
            )

        file_name = get_file_name(audio)
        file_path = await converter.convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name))
            else file_name
        )
    elif url:
        file_path = await converter.convert(youtube.download(url))
    else:
        return await lel.edit_text("❗ Anda tidak memberi saya apa pun untuk dimainkan!")

    if message.chat.id in callsmusic.pytgcalls.active_calls:
        position = await queues.put(message.chat.id, file=file_path)
        await lel.edit(
            f"🎧 **Lagi Dipilih!\n"
            f"⚡ **Antrian ke:** {position} \n"
            "📱 **Requested by:** {}".format(message.from_user.mention()),
        )
    else:
        callsmusic.pytgcalls.join_group_call(message.chat.id, file_path)
        await message.reply_photo(
            photo="https://telegra.ph/file/811ef614f43cada3bc44b.jpg",
            reply_markup=keyboard,
            caption=f"⚡ **Lagu Dimainkan!**\n"
            "📱 **Requested by**: {}".format(message.from_user.mention()),
        )
        return await lel.delete()
