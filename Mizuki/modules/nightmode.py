from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telethon import *
from telethon import functions
from telethon.tl.types import ChatBannedRights

from Mizuki import OWNER_ID, tbot
from Mizuki.events import register
from Mizuki.modules.sql.nightmode_sql import (
    add_nightmode,
    get_all_chat_id,
    is_nightmode_indb,
    rmnightmode,
)

hehes = ChatBannedRights(
    until_date=None,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    send_polls=True,
    invite_users=True,
    pin_messages=True,
    change_info=True,
)
openhehe = ChatBannedRights(
    until_date=None,
    send_messages=False,
    send_media=False,
    send_stickers=False,
    send_gifs=False,
    send_games=False,
    send_inline=False,
    send_polls=False,
    invite_users=True,
    pin_messages=True,
    change_info=True,
)


async def is_register_admin(chat, user):
    if isinstance(chat, (types.InputPeerChannel, types.InputChannel)):
        return isinstance(
            (
                await tbot(functions.channels.GetParticipantRequest(chat, user))
            ).participant,
            (types.ChannelParticipantAdmin, types.ChannelParticipantCreator),
        )
    if isinstance(chat, types.InputPeerUser):
        return True


async def can_change_info(message):
    result = await tbot(
        functions.channels.GetParticipantRequest(
            channel=message.chat_id,
            user_id=message.sender_id,
        )
    )
    p = result.participant
    return isinstance(p, types.ChannelParticipantCreator) or (
        isinstance(p, types.ChannelParticipantAdmin) and p.admin_rights.change_info
    )


@register(pattern="^/(nightmode|Nightmode|NightMode) ?(.*)")
async def profanity(event):
    if event.fwd_from:
        return
    if event.is_private:
        return
    input = event.pattern_match.group(2)
    if not event.sender_id == OWNER_ID:
        if not await is_register_admin(event.input_chat, event.sender_id):
            await event.reply("Only admins can execute this command!")
            return
    if not input:
        if is_nightmode_indb(str(event.chat_id)):
            await event.reply("Currently Night Mode is Enabled for this Chat.")
            return
        await event.reply("Currently Night Mode is Disabled for this Chat.")
        return
    if "on" in input:
        if event.is_group:
            if is_nightmode_indb(str(event.chat_id)):
                await event.reply("Night Mode is Already Turned ON for this Chat.")
                return
            add_nightmode(str(event.chat_id))
            await event.reply("Night Mode turned on for this chat.")
    if "off" in input:
        if event.is_group:
            if not is_nightmode_indb(str(event.chat_id)):
                await event.reply("Night Mode is Already Off for this Chat.")
                return
        rmnightmode(str(event.chat_id))
        await event.reply("Night Mode Disabled!")
    if not "off" in input and not "on" in input:
        await event.reply("Please Specify On or Off!")
        return


async def job_close():
    chats = get_all_chat_id()
    if len(chats) == 0:
        return
    for pro in chats:
        try:
            await tbot.send_message(
                int(pro.chat_id),
                "12:00 Am, Group Is Closing Till 6 Am. Night Mode Started! \n**Powered By Mizuki**",
            )
            await tbot(
                functions.messages.EditChatDefaultBannedRightsRequest(
                    peer=int(pro.chat_id), banned_rights=hehes
                )
            )
        except Exception as e:
            logger.info(f"Unable To Close Group {chat} > {e}")


# Run everyday at 12am
scheduler = AsyncIOScheduler(timezone="Asia/Kolkata")
scheduler.add_job(job_close, trigger="cron", hour=23, minute=59)
scheduler.start()


async def job_open():
    chats = get_all_chat_id()
    if len(chats) == 0:
        return
    for pro in chats:
        try:
            await tbot.send_message(
                int(pro.chat_id), "06:00 Am, Group Is Opening.\n**Powered By Mizuki**"
            )
            await tbot(
                functions.messages.EditChatDefaultBannedRightsRequest(
                    peer=int(pro.chat_id), banned_rights=openhehe
                )
            )
        except Exception as e:
            logger.info(f"Unable To Open Group {pro.chat_id} - {e}")


# Run everyday at 06
scheduler = AsyncIOScheduler(timezone="Asia/Kolkata")
scheduler.add_job(job_open, trigger="cron", hour=5, minute=58)
scheduler.start()

__help__ = """
*Night Mode for prevent night spam on groups*

• `/nightmode on/off`*:* Night Mode chats get automatically closed at 12pm and automatically opened at 6am to prevent night spams.
"""

__mod_name__ = "Night Mode"
