import requests
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from youtube_search import YoutubeSearch

import converter
from callsmusic import callsmusic, queues
from downloaders import youtube
from helpers.decorators import authorized_users_only, errors
from helpers.filters import command, other_filters
from Mizuki import Client


@Client.on_message(command("yt") & other_filters)
@errors
@authorized_users_only
async def play(_, message: Message):

    lel = await message.reply("🔥 **Menemukan Lagu**...")
    message.from_user.id
    user_id = message.from_user.id
    message.from_user.first_name
    user_name = message.from_user.first_name
    rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"

    query = ""
    for i in message.command[1:]:
        query += " " + str(i)
    print(query)
    await lel.edit("🌈 **Memproses Lagu**...")
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        url = f"https://youtube.com{results[0]['url_suffix']}"
        # print(results)
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"thumb{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)

        results[0]["duration"]
        results[0]["url_suffix"]
        results[0]["views"]

    except Exception as e:
        lel.edit(
            "‼️ **Lagu tidak ditemukan**.\n\nCoba ketik penyanyi dan judul lagunya dengan lengkap."
        )
        print(str(e))
        return

    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text="🖥 Tonton Di YouTube", url=f"{url}")],
            [
                InlineKeyboardButton(
                    text="join me if you're sad", url="https://t.me/hbreakclub"
                )
            ],
        ]
    )

    keyboard2 = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text="🖥 Tonton Di YouTube", url=f"{url}")],
            [
                InlineKeyboardButton(
                    text="join me if you're sad", url="https://t.me/hbreakclub"
                )
            ],
        ]
    )

    audio = (
        (message.reply_to_message.audio or message.reply_to_message.voice)
        if message.reply_to_message
        else None
    )

    if audio:
        await lel.edit_text("Lel")

    elif url:
        file_path = await converter.convert(youtube.download(url))
    else:
        return await lel.edit_text("❗ Anda tidak memberi saya apa pun untuk dimainkan!")

    if message.chat.id in callsmusic.pytgcalls.active_calls:
        position = await queues.put(message.chat.id, file=file_path)
        await message.reply_photo(
            photo=thumb_name,
            caption=f"🎧 **Song:** [{title}]({url}) \n"
            f"⚡ **Antrian ke:** {position} \n"
            "📱 **Requested by:** {}".format(message.from_user.mention()),
            reply_markup=keyboard2,
        )
        return await lel.delete()
    else:
        callsmusic.pytgcalls.join_group_call(message.chat.id, file_path)
        await message.reply_photo(
            photo=thumb_name,
            reply_markup=keyboard,
            caption=f"⚡ **Song:** [{title}]({url}).\n"
            "📱 **Requested by**: {}".format(message.from_user.mention()),
        )
        return await lel.delete()
