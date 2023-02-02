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

import re
import random
import nonebot
import requests
import unicodedata

try:
    import ujson as json
except ModuleNotFoundError:
    import json

from .utils import MirlKoi,Anosu,Lolicon,is_MirlKoi_tag

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
            if not Tag:
                msg,image_list = MirlKoi(N,Tag,R18)
                api = "MirlKoi API"
            else:
                tag = is_MirlKoi_tag(Tag)
                if tag:
                    msg,image_list = MirlKoi(N,tag,R18)
                    api = "MirlKoi API"
                else:
                    msg,image_list = Anosu(N,Tag,R18)
                    api = "Jitsu"
    else:
        msg,image_list = Lolicon(N,Tag,R18)
        api = "Lolicon API"

    msg = msg.replace("Bot_NICKNAME",Bot_NICKNAME)

    msg += f"\n图片取自：{api}"
    if image_list:
        if N <= 3:
            image = Message()
            for i in range(N):
                image +=  MessageSegment.image(file = image_list[i])
            await setu.finish(Message(msg) + image, at_sender = True)
        else:
            await setu.send(msg, at_sender = True)
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
    else:
        await setu.finish(msg, at_sender = True)
