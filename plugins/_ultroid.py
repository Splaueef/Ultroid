# Ultroid - UserBot
# Copyright (C) 2021-2026 TeamUltroid
#
# This file is a part of < https://github.com/Splaueef/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/Splaueef/Ultroid/blob/main/LICENSE/>.

from telethon.errors import (
    BotMethodInvalidError,
    ChatSendInlineForbiddenError,
    ChatSendMediaForbiddenError,
)

from . import LOG_CHANNEL, LOGS, Button, asst, eor, get_string, ultroid_cmd

REPOMSG = """
• **ULTROID USERBOT** •\n
• Repo - [Click Here](https://github.com/Splaueef/Ultroid)
• Addons - [Click Here](https://github.com/Splaueef/UltroidAddons)
• Support - @UltroidSupportChat
"""

RP_BUTTONS = [
    [
        Button.url(get_string("bot_3"), "https://github.com/Splaueef/Ultroid"),
        Button.url(get_string("btn_addons"), "https://github.com/Splaueef/UltroidAddons"),
    ],
    [Button.url(get_string("btn_support_group"), "t.me/UltroidSupportChat")],
]

ULTSTRING = """🎇 **Thanks for Deploying Ultroid Userbot!**

• Here, are the Some Basic stuff from, where you can Know, about its Usage."""


@ultroid_cmd(
    pattern="repo$",
    manager=True,
)
async def repify(e):
    try:
        q = await e.client.inline_query(asst.me.username, "")
        await q[0].click(e.chat_id)
        return await e.delete()
    except (
        ChatSendInlineForbiddenError,
        ChatSendMediaForbiddenError,
        BotMethodInvalidError,
    ):
        pass
    except Exception as er:
        LOGS.info(f"Error while repo command : {str(er)}")
    await e.eor(REPOMSG)


@ultroid_cmd(pattern="ultroid$")
async def useUltroid(rs):
    button = Button.inline(get_string("btn_start"), "initft_2")
    msg = await asst.send_message(
        LOG_CHANNEL,
        ULTSTRING,
        file="https://graph.org/file/54a917cc9dbb94733ea5f.jpg",
        buttons=button,
    )
    if not (rs.chat_id == LOG_CHANNEL and rs.client._bot):
        await eor(rs, f"**[Click Here]({msg.message_link})**")
