# Ultroid - UserBot
# Copyright (C) 2021-2026 TeamUltroid
#
# This file is a part of < https://github.com/Splaueef/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/Splaueef/Ultroid/blob/main/LICENSE/>.

import base64
import inspect
from datetime import datetime
from html import unescape
from random import choice
from re import compile as re_compile

from bs4 import BeautifulSoup as bs
from telethon import Button
from telethon.tl.alltlobjects import LAYER, tlobjects
from telethon.tl.types import DocumentAttributeAudio as Audio
from telethon.tl.types import InputWebDocument as wb

from pyUltroid.fns.misc import google_search
from pyUltroid.fns.tools import (
    _webupload_cache,
    async_searcher,
    get_ofox,
    saavn_search,
    webuploader,
)

from . import *
from . import _ult_cache

SUP_BUTTONS = [
    [
        Button.url("• Repo •", url="https://github.com/Splaueef/Ultroid"),
        Button.url("• Support •", url="t.me/UltroidSupportChat"),
    ],
]

ofox = "https://graph.org/file/231f0049fcd722824f13b.jpg"
gugirl = "https://graph.org/file/0df54ae4541abca96aa11.jpg"
ultpic = "https://graph.org/file/4136aa1650bc9d4109cc5.jpg"

apis = [
    "QUl6YVN5QXlEQnNZM1dSdEI1WVBDNmFCX3c4SkF5NlpkWE5jNkZV",
    "QUl6YVN5QkYwenhMbFlsUE1wOXh3TVFxVktDUVJxOERnZHJMWHNn",
    "QUl6YVN5RGRPS253blB3VklRX2xiSDVzWUU0Rm9YakFLSVFWMERR",
]


@in_pattern("ofox", owner=True)
async def _(e):
    try:
        match = e.text.split(" ", maxsplit=1)[1]
    except IndexError:
        kkkk = e.builder.article(
            title="Enter Device Codename",
            thumb=wb(ofox, 0, "image/jpeg", []),
            text="**OFᴏx🦊Rᴇᴄᴏᴠᴇʀʏ**\n\nYou didn't search anything",
            buttons=Button.switch_inline("Sᴇᴀʀᴄʜ Aɢᴀɪɴ", query="ofox ", same_peer=True),
        )
        return await e.answer([kkkk])
    device, releases = await get_ofox(match)
    if device.get("detail") is None:
        fox = []
        fullname = device["full_name"]
        codename = device["codename"]
        str(device["supported"])
        maintainer = device["maintainer"]["name"]
        link = f"https://orangefox.download/device/{codename}"
        for data in releases["data"]:
            release = data["type"]
            version = data["version"]
            size = humanbytes(data["size"])
            release_date = datetime.utcfromtimestamp(data["date"]).strftime("%Y-%m-%d")
            text = f"[­]({ofox})**OrangeFox Recovery For**\n\n"
            text += f"`  Full Name: {fullname}`\n"
            text += f"`  Codename: {codename}`\n"
            text += f"`  Maintainer: {maintainer}`\n"
            text += f"`  Build Type: {release}`\n"
            text += f"`  Version: {version}`\n"
            text += f"`  Size: {size}`\n"
            text += f"`  Build Date: {release_date}`"
            fox.append(
                await e.builder.article(
                    title=f"{fullname}",
                    description=f"{version}\n{release_date}",
                    text=text,
                    thumb=wb(ofox, 0, "image/jpeg", []),
                    link_preview=True,
                    buttons=[
                        Button.url("Dᴏᴡɴʟᴏᴀᴅ", url=f"{link}"),
                        Button.switch_inline(
                            "Sᴇᴀʀᴄʜ Aɢᴀɪɴ", query="ofox ", same_peer=True
                        ),
                    ],
                )
            )
        await e.answer(
            fox, switch_pm="OrangeFox Recovery Search.", switch_pm_param="start"
        )
    else:
        await e.answer(
            [], switch_pm="OrangeFox Recovery Search.", switch_pm_param="start"
        )


@in_pattern("fl2lnk ?(.*)", owner=True)
async def _(e):
    match = e.pattern_match.group(1)
    chat_id, msg_id = match.split(":")
    filename = _webupload_cache[int(chat_id)][int(msg_id)]
    if "/" in filename:
        filename = filename.split("/")[-1]
    __cache = f"{chat_id}:{msg_id}"
    buttons = [
        [
            Button.inline("anonfiles", data=f"flanonfiles//{__cache}"),
            Button.inline("transfer", data=f"fltransfer//{__cache}"),
        ],
        [
            Button.inline("bayfiles", data=f"flbayfiles//{__cache}"),
            Button.inline("x0.at", data=f"flx0.at//{__cache}"),
        ],
        [
            Button.inline("file.io", data=f"flfile.io//{__cache}"),
            Button.inline("siasky", data=f"flsiasky//{__cache}"),
        ],
    ]
    try:
        lnk = [
            await e.builder.article(
                title=f"Upload {filename}",
                text=f"**File:**\n{filename}",
                buttons=buttons,
            )
        ]
    except BaseException as er:
        LOGS.exception(er)
        lnk = [
            await e.builder.article(
                title="fl2lnk",
                text="File not found",
            )
        ]
    await e.answer(lnk, switch_pm="File to Link.", switch_pm_param="start")


@callback(
    re_compile(
        "fl(.*)",
    ),
    owner=True,
)
async def _(e):
    t = (e.data).decode("UTF-8")
    data = t[2:]
    host = data.split("//")[0]
    chat_id, msg_id = data.split("//")[1].split(":")
    filename = _webupload_cache[int(chat_id)][int(msg_id)]
    if "/" in filename:
        filename = filename.split("/")[-1]
    await e.edit(f"Uploading `{filename}` on {host}")
    link = (await webuploader(chat_id, msg_id, host)).strip().replace("\n", "")
    await e.edit(f"Uploaded `{filename}` on {host}.", buttons=Button.url("View", link))


@in_pattern("repo", owner=True)
async def repo(e):
    res = [
        await e.builder.article(
            title="Ultroid Userbot",
            description="Userbot | Telethon",
            thumb=wb(ultpic, 0, "image/jpeg", []),
            text="• **ULTROID USERBOT** •",
            buttons=SUP_BUTTONS,
        ),
    ]
    await e.answer(res, switch_pm="Ultroid Repo.", switch_pm_param="start")


@in_pattern("go", owner=True)
async def gsearch(q_event):
    try:
        match = q_event.text.split(maxsplit=1)[1]
    except IndexError:
        return await q_event.answer(
            [], switch_pm="Google Search. Enter a query!", switch_pm_param="start"
        )
    searcher = []
    gresults = await google_search(match)
    for i in gresults:
        try:
            title = i["title"]
            link = i["link"]
            desc = i["description"]
            searcher.append(
                await q_event.builder.article(
                    title=title,
                    description=desc,
                    thumb=wb(gugirl, 0, "image/jpeg", []),
                    text=f"**Google Search**\n\n**• Title •**\n`{title}`\n\n**• Description •**\n`{desc}`",
                    link_preview=False,
                    buttons=[
                        [Button.url("Link", url=f"{link}")],
                        [
                            Button.switch_inline(
                                "Search Again",
                                query="go ",
                                same_peer=True,
                            ),
                            Button.switch_inline(
                                "Share",
                                query=f"go {match}",
                                same_peer=False,
                            ),
                        ],
                    ],
                ),
            )
        except IndexError:
            break
    await q_event.answer(searcher, switch_pm="Google Search.", switch_pm_param="start")


@in_pattern("mods", owner=True)
async def _(e):
    try:
        quer = e.text.split(" ", maxsplit=1)[1]
    except IndexError:
        return await e.answer(
            [], switch_pm="Mod Apps Search. Enter app name!", switch_pm_param="start"
        )
    start = 0 * 3 + 1
    da = base64.b64decode(choice(apis)).decode("ascii")
    url = f"https://www.googleapis.com/customsearch/v1?key={da}&cx=25b3b50edb928435b&q={quer}&start={start}"
    data = await async_searcher(url, re_json=True)
    search_items = data.get("items", [])
    modss = []
    for a in search_items:
        title = a.get("title")
        desc = a.get("snippet")
        link = a.get("link")
        text = f"**••Tɪᴛʟᴇ••** `{title}`\n\n"
        text += f"**Dᴇsᴄʀɪᴘᴛɪᴏɴ** `{desc}`"
        modss.append(
            await e.builder.article(
                title=title,
                description=desc,
                text=text,
                link_preview=True,
                buttons=[
                    [Button.url("Dᴏᴡɴʟᴏᴀᴅ", url=f"{link}")],
                    [
                        Button.switch_inline(
                            "Mᴏʀᴇ Mᴏᴅs",
                            query="mods ",
                            same_peer=True,
                        ),
                        Button.switch_inline(
                            "Sʜᴀʀᴇ",
                            query=f"mods {quer}",
                            same_peer=False,
                        ),
                    ],
                ],
            ),
        )
    await e.answer(modss, switch_pm="Search Mod Applications.", switch_pm_param="start")


APP_CACHE = {}
RECENTS = {}
PLAY_API = "https://googleplay.onrender.com/api/apps?q="


@in_pattern("app", owner=True)
async def _(e):
    try:
        f = e.text.split(maxsplit=1)[1].lower()
    except IndexError:
        get_string("instu_1")
        res = []
        if APP_CACHE and RECENTS.get(e.sender_id):
            res.extend(
                APP_CACHE[a][0] for a in RECENTS[e.sender_id] if APP_CACHE.get(a)
            )
        return await e.answer(
            res, switch_pm=get_string("instu_2"), switch_pm_param="start"
        )
    try:
        return await e.answer(
            APP_CACHE[f], switch_pm="Application Searcher.", switch_pm_param="start"
        )
    except KeyError:
        pass
    foles = []
    url = PLAY_API + f.replace(" ", "+")
    aap = await async_searcher(url, re_json=True)
    for z in aap["results"][:50]:
        url = "https://play.google.com/store/apps/details?id=" + z["appId"]
        name = z["title"]
        desc = unescape(z["summary"])[:300].replace("<br>", "\n") + "..."
        dev = z["developer"]["devId"]
        text = f"**• App Name •** [{name}]({url})\n"
        text += f"**• Developer •** `{dev}`\n"
        text += f"**• Description •**\n`{desc}`"
        foles.append(
            await e.builder.article(
                title=name,
                description=dev,
                thumb=wb(z["icon"], 0, "image/jpeg", []),
                text=text,
                link_preview=True,
                buttons=[
                    [Button.url("Link", url=url)],
                    [
                        Button.switch_inline(
                            "More Apps",
                            query="app ",
                            same_peer=True,
                        ),
                        Button.switch_inline(
                            "Sʜᴀʀᴇ",
                            query=f"app {f}",
                            same_peer=False,
                        ),
                    ],
                ],
            ),
        )
    APP_CACHE.update({f: foles})
    if RECENTS.get(e.sender_id):
        RECENTS[e.sender_id].append(f)
    else:
        RECENTS.update({e.sender_id: [f]})
    await e.answer(foles, switch_pm="Application Searcher.", switch_pm_param="start")


PISTON_URI = "https://emkc.org/api/v2/piston/"
PISTON_LANGS = {}


@in_pattern("run", owner=True)
async def piston_run(event):
    try:
        lang = event.text.split()[1]
        code = event.text.split(maxsplit=2)[2]
    except IndexError:
        result = await event.builder.article(
            title="Bad Query",
            description="Usage: [Language] [code]",
            thumb=wb(
                "https://graph.org/file/e33c57fc5f1044547e4d8.jpg", 0, "image/jpeg", []
            ),
            text=f'**Inline Usage**\n\n`@{asst.me.username} run python print("hello world")`\n\n[Language List](https://graph.org/Ultroid-09-01-6)',
        )
        return await event.answer([result])
    if not PISTON_LANGS:
        se = await async_searcher(f"{PISTON_URI}runtimes", re_json=True)
        PISTON_LANGS.update({lang.pop("language"): lang for lang in se})
    if lang in PISTON_LANGS.keys():
        version = PISTON_LANGS[lang]["version"]
    else:
        result = await event.builder.article(
            title="Unsupported Language",
            description="Usage: [Language] [code]",
            thumb=wb(
                "https://graph.org/file/e33c57fc5f1044547e4d8.jpg", 0, "image/jpeg", []
            ),
            text=f'**Inline Usage**\n\n`@{asst.me.username} run python print("hello world")`\n\n[Language List](https://graph.org/Ultroid-09-01-6)',
        )
        return await event.answer([result])
    output = await async_searcher(
        f"{PISTON_URI}execute",
        post=True,
        json={
            "language": lang,
            "version": version,
            "files": [{"content": code}],
        },
        re_json=True,
    )

    output = output["run"]["output"] or get_string("instu_4")
    if len(output) > 3000:
        output = f"{output[:3000]}..."
    result = await event.builder.article(
        title="Result",
        description=output,
        text=f"• **Language:**\n`{lang}`\n\n• **Code:**\n`{code}`\n\n• **Result:**\n`{output}`",
        thumb=wb(
            "https://graph.org/file/871ee4a481f58117dccc4.jpg", 0, "image/jpeg", []
        ),
        buttons=Button.switch_inline("Fork", query=event.text, same_peer=True),
    )
    await event.answer([result], switch_pm="• Piston •", switch_pm_param="start")


FDROID_ = {}


@in_pattern("fdroid", owner=True)
async def do_magic(event):
    try:
        match = event.text.split(" ", maxsplit=1)[1].lower()
    except IndexError:
        return await event.answer(
            [], switch_pm="Enter Query to Search", switch_pm_param="start"
        )
    if FDROID_.get(match):
        return await event.answer(
            FDROID_[match], switch_pm=f"• Results for {match}", switch_pm_param="start"
        )
    link = "https://search.f-droid.org/?q=" + match.replace(" ", "+")
    content = await async_searcher(link, re_content=True)
    BSC = bs(content, "html.parser", from_encoding="utf-8")
    ress = []
    for dat in BSC.find_all("a", "package-header")[:10]:
        image = dat.find("img", "package-icon")["src"]
        if image.endswith("/"):
            image = "https://graph.org/file/a8dd4a92c5a53a89d0eff.jpg"
        title = dat.find("h4", "package-name").text.strip()
        desc = dat.find("span", "package-summary").text.strip()
        text = f"• **Name :** `{title}`\n\n"
        text += f"• **Description :** `{desc}`\n"
        text += f"• **License :** `{dat.find('span', 'package-license').text.strip()}`"
        imga = wb(image, 0, "image/jpeg", [])
        ress.append(
            await event.builder.article(
                title=title,
                type="photo",
                description=desc,
                text=text,
                content=imga,
                thumb=imga,
                include_media=True,
                buttons=[
                    Button.inline(
                        "• Download •", "fd" + dat["href"].split("packages/")[-1]
                    ),
                    Button.switch_inline("• Share •", query=event.text),
                ],
            )
        )
    msg = f"Showing {len(ress)} Results!" if ress else "No Results Found"
    FDROID_.update({match: ress})
    await event.answer(ress, switch_pm=msg, switch_pm_param="start")


# Thanks to OpenSource
_bearer_collected = [
    "AAAAAAAAAAAAAAAAAAAAALIKKgEAAAAA1DRuS%2BI7ZRKiagD6KHYmreaXomo%3DP5Vaje4UTtEkODg0fX7nCh5laSrchhtLxeyEqxXpv0w9ZKspLD",
    "AAAAAAAAAAAAAAAAAAAAAL5iUAEAAAAAmo6FYRjqdKlI3cNziIm%2BHUQB9Xs%3DS31pj0mxARMTOk2g9dvQ1yP9wknvY4FPBPUlE00smJcncw4dPR",
    "AAAAAAAAAAAAAAAAAAAAAN6sVgEAAAAAMMjMMWrwgGyv7YQOWN%2FSAsO5SGM%3Dg8MG9Jq93Rlllaok6eht7HvRCruN4Vpzp4NaVsZaaHHWSTzKI8",
]


@in_pattern("twitter", owner=True)
async def twitter_search(event):
    try:
        match = event.text.split(maxsplit=1)[1].lower()
    except IndexError:
        return await event.answer(
            [], switch_pm="Enter Query to Search", switch_pm_param="start"
        )
    try:
        return await event.answer(
            _ult_cache["twitter"][match],
            switch_pm="• Twitter Search •",
            switch_pm_param="start",
        )
    except KeyError:
        pass
    headers = {"Authorization": f"bearer {choice(_bearer_collected)}"}
    res = await async_searcher(
        f"https://api.twitter.com/1.1/users/search.json?q={match}",
        headers=headers,
        re_json=True,
    )
    reso = []
    for user in res:
        thumb = wb(user["profile_image_url_https"], 0, "image/jpeg", [])
        if user.get("profile_banner_url"):
            url = user["profile_banner_url"]
            text = f"[\xad]({url})• **Name :** `{user['name']}`\n"
        else:
            text = f"• **Name :** `{user['name']}`\n"
        text += f"• **Description :** `{user['description']}`\n"
        text += f"• **Username :** `@{user['screen_name']}`\n"
        text += f"• **Followers :** `{user['followers_count']}`    • **Following :** `{user['friends_count']}`\n"
        pro_ = "https://twitter.com/" + user["screen_name"]
        text += f"• **Link :** [Click Here]({pro_})\n_"
        reso.append(
            await event.builder.article(
                title=user["name"],
                description=user["description"],
                url=pro_,
                text=text,
                thumb=thumb,
            )
        )
    swi_ = f"🐦 Showing {len(reso)} Results!" if reso else "No User Found :("
    await event.answer(reso, switch_pm=swi_, switch_pm_param="start")
    if _ult_cache.get("twitter"):
        _ult_cache["twitter"].update({match: reso})
    else:
        _ult_cache.update({"twitter": {match: reso}})


_savn_cache = {}


@in_pattern("saavn", owner=True)
async def savn_s(event):
    try:
        query = event.text.split(maxsplit=1)[1].lower()
    except IndexError:
        return await event.answer(
            [], switch_pm="Enter Query to search 🔍", switch_pm_param="start"
        )
    if query in _savn_cache:
        return await event.answer(
            _savn_cache[query],
            switch_pm=f"Showing Results for {query}",
            switch_pm_param="start",
        )
    results = await saavn_search(query)
    swi = "🎵 Saavn Search" if results else "No Results Found!"
    res = []
    for song in results:
        thumb = wb(song["image"], 0, "image/jpeg", [])
        text = f"• **Title :** {song['title']}"
        text += f"\n• **Year :** {song['year']}"
        text += f"\n• **Lang :** {song['language']}"
        text += f"\n• **Artist :** {song['artists']}"
        text += f"\n• **Release Date :** {song['release_date']}"
        res.append(
            await event.builder.article(
                title=song["title"],
                description=song["artists"],
                type="audio",
                text=text,
                include_media=True,
                buttons=Button.switch_inline(
                    "Search Again 🔍", query="saavn", same_peer=True
                ),
                thumb=thumb,
                content=wb(
                    song["url"],
                    0,
                    "audio/mp4",
                    [
                        Audio(
                            title=song["title"],
                            duration=int(song["duration"]),
                            performer=song["artists"],
                        )
                    ],
                ),
            )
        )
    await event.answer(res, switch_pm=swi, switch_pm_param="start")
    _savn_cache.update({query: res})


@in_pattern("tl", owner=True)
async def inline_tl(ult):
    try:
        match = ult.text.split(maxsplit=1)[1]
    except IndexError:
        text = f"**Telegram TlObjects Searcher.**\n__(Don't use if you don't know what it is!)__\n\n• Example Usage\n`@{asst.me.username} tl GetFullUserRequest`"
        return await ult.answer(
            [
                await ult.builder.article(
                    title="How to Use?",
                    description="Tl Searcher by Ultroid",
                    url="https://t.me/TeamUltroid",
                    text=text,
                )
            ],
            switch_pm="Tl Search 🔍",
            switch_pm_param="start",
        )
    res = []
    for key in tlobjects.values():
        if match.lower() in key.__name__.lower():
            tyyp = "Function" if "tl.functions." in str(key) else "Type"
            text = f"**Name:** `{key.__name__}`\n"
            text += f"**Category:** `{tyyp}`\n"
            text += f"\n`from {key.__module__} import {key.__name__}`\n\n"
            if args := str(inspect.signature(key))[1:][:-1]:
                text += "**Parameter:**\n"
                for para in args.split(","):
                    text += " " * 4 + "`" + para + "`\n"
            text += f"\n**Layer:** `{LAYER}`"
            res.append(
                await ult.builder.article(
                    title=key.__name__,
                    description=tyyp,
                    url="https://t.me/TeamUltroid",
                    text=text[:4000],
                )
            )
    mo = f"Showing {len(res)} results!" if res else f"No Results for {match}!"
    await ult.answer(res[:50], switch_pm=mo, switch_pm_param="start")


InlinePlugin.update(
    {
        "Pʟᴀʏ Sᴛᴏʀᴇ Aᴘᴘs": "app telegram",
        "Mᴏᴅᴅᴇᴅ Aᴘᴘs": "mods minecraft",
        "Sᴇᴀʀᴄʜ Oɴ Gᴏᴏɢʟᴇ": "go TeamUltroid",
        "WʜɪSᴘᴇʀ": "wspr @username Hello🎉",
        "YᴏᴜTᴜʙᴇ Dᴏᴡɴʟᴏᴀᴅᴇʀ": "yt Ed Sheeran Perfect",
        "Piston Eval": "run javascript console.log('Hello Ultroid')",
        "OʀᴀɴɢᴇFᴏx🦊": "ofox beryllium",
        "Tᴡɪᴛᴛᴇʀ Usᴇʀ": "twitter theultroid",
        "Fᴅʀᴏɪᴅ Sᴇᴀʀᴄʜ": "fdroid telegram",
        "Sᴀᴀᴠɴ sᴇᴀʀᴄʜ": "saavn",
        "Tʟ Sᴇᴀʀᴄʜ": "tl",
    }
)
