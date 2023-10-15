from nonebot.plugin.on import on_regex,on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import (
    Bot,
    MessageEvent,
    GroupMessageEvent,
    PrivateMessageEvent,
    MessageSegment,
    Message
    )
from nonebot.params import CommandArg,Arg

import nonebot
import re
import httpx
import asyncio
import unicodedata

from .api.MirlKoi import MirlKoi,is_MirlKoi_tag
from .api.Anosu import Anosu
from .api.Lolicon import Lolicon

Bot_NICKNAME = list(nonebot.get_driver().config.nickname)

Bot_NICKNAME = Bot_NICKNAME[0] if Bot_NICKNAME else "色图bot"

hello = on_command("色图", aliases = {"涩图"}, rule = to_me(), priority = 50, block = True)

@hello.handle()
async def _(bot: Bot, event: MessageEvent):
    msg = (
        "发送【我要一张xx涩图】可获得一张随机色图。"
        "群聊图片取自：\n"
        "Jitsu：https://image.anosu.top/\n"
        "MirlKoi API：https://iw233.cn/\n"
        "私聊图片取自：\n"
        "Lolicon API：https://api.lolicon.app/"
        )
    await hello.finish(msg)

async def func(client,url):
    resp = await client.get(url,headers={'Referer':'http://www.weibo.com/',})
    if resp.status_code == 200:
        return resp.content
    else:
        return None

setu = on_regex("^(我?要|来).*[张份].+$", priority = 50, block = True)

@setu.handle()
async def _(bot: Bot, event: MessageEvent):
    msg = ""
    cmd = event.get_plaintext()
    N = re.sub(r'^我?要|^来|[张份].+$', '', cmd)
    N = N if N else 1

    try:
        N = int(N)
    except ValueError:
        try:
            N = int(unicodedata.numeric(N))
        except (TypeError, ValueError):
            N = 0

    Tag = re.sub(r'^我?要|^来|.*[张份]', '', cmd)
    Tag = Tag [:-2]if (Tag.endswith("涩图") or Tag.endswith("色图")) else Tag

    if Tag.startswith("r18"):
        Tag = Tag [3:]
        R18 = 1
    else:
        R18 = 0

    if isinstance(event,GroupMessageEvent):
        if R18:
            await setu.finish("涩涩是禁止事项！！")
        else:
            if not Tag or is_MirlKoi_tag(Tag):
                api = "MirlKoi API"
                setufunc = MirlKoi
            else:
                api = "Jitsu"
                setufunc = Anosu
    else:
        api = customer_api.get(str(event.user_id),None)
        if api == "Lolicon API":
            setufunc = Lolicon
        else:
            if not R18 or not Tag or is_MirlKoi_tag(Tag):
                api = "MirlKoi API"
                setufunc = MirlKoi
            else:
                api = "Jitsu"
                setufunc = Anosu

    msg,url_list = await setufunc(N,Tag,R18)
    msg = msg.replace("Bot_NICKNAME",Bot_NICKNAME) + f"\n图片取自：{api}\n"

    if len(url_list) >3:
        msg = msg[:-1]
        await setu.send(msg, at_sender = True)

    async with httpx.AsyncClient() as client:
        task_list = []
        for url in url_list:
            task = asyncio.create_task(func(client,url))
            task_list.append(task)
        image_list = await asyncio.gather(*task_list)

    image_list = [image for image in image_list if image]

    if not image_list:
        await setu.finish(msg + "获取图片失败。", at_sender = True)
    N = len(image_list)
    if N <= 3:
        image = Message()
        for i in range(N):
            image +=  MessageSegment.image(file = image_list[i])
        await setu.finish(Message(msg) + image, at_sender = True)
    else:
        msg_list =[]
        for i in range(N):
            msg_list.append(
                {
                    "type": "node",
                    "data": {
                        "name": Bot_NICKNAME,
                        "uin": event.self_id,
                        "content": MessageSegment.image(file = image_list[i])
                        }
                    }
                )
        if isinstance(event,GroupMessageEvent):
            await bot.send_group_forward_msg(group_id = event.group_id, messages = msg_list)
        else:
            await bot.send_private_forward_msg(user_id = event.user_id, messages = msg_list)

import os
from pathlib import Path

try:
    import ujson as json
except ModuleNotFoundError:
    import json

path = Path() / "data" / "setu"
file = path / "customer_api.json"
if file.exists():
    with open(file, "r", encoding="utf8") as f:
        customer_api = json.load(f)
else:
    customer_api = {}
    if not path.exists():
        os.makedirs(path)

set_api = on_command("设置api", aliases = {"切换api","指定api"}, priority = 50, block = True)

@set_api.got(
    "api",
    prompt = (
        "请选择:\n"
        "1.Jitsu/MirlKoi API\n"
        "2.Lolicon API"
        )
    )
async def _(event: PrivateMessageEvent, api: Message = Arg()):
    api = str(api)
    user_id = str(event.user_id)
    def save():
        with open(file, "w", encoding="utf8") as f:
            json.dump(customer_api, f, ensure_ascii=False, indent=4)
    if api == "1":
        customer_api[user_id] = "Jitsu/MirlKoi API"
        save()
        await set_api.finish("api已切换为Jitsu/MirlKoi API")
    elif api == "2":
        customer_api[user_id] = "Lolicon API"
        save()
        await set_api.finish("api已切换为Lolicon API")
    else:
        await set_api.finish("api设置失败")

