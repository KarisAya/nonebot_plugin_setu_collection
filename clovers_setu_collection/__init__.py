import re
from clovers.core.plugin import Plugin, Event, Result
from clovers.utils.tools import to_int, download_url
from .api.MirlKoi import MirlKoi, is_MirlKoi_tag
from .api.Anosu import Anosu

plugin = Plugin()


@plugin.handle({"涩图，色图"}, ["to_me"])
async def _(event: Event):
    if not event.kwargs["to_me"]:
        return
    msg = (
        "发送【我要一张xx涩图】可获得一张随机色图。"
        "群聊图片取自：\n"
        "Jitsu：https://image.anosu.top/\n"
        "MirlKoi API：https://iw233.cn/\n"
        "私聊图片取自：\n"
        "Lolicon API：https://api.lolicon.app/"
    )
    return Result("text", msg)


@plugin.handle(r"来(.*)[张份]([rR]18)?(.+)$", ["Bot_Nickname", "group_id", "user_id"])
async def _(event: Event) -> Result:
    Bot_Nickname = event.kwargs["Bot_Nickname"]
    n, r18, tag = event.args
    if n:
        n = to_int(n)
        if n is None:
            return
    else:
        n = 1
    if tag[-2:] in {"色图", "涩图", "图片"}:
        tag = tag[:-2]
    resp = []
    if n > 5:
        n = 5
        resp.append("最多可以点5张图片哦")

    resp.append(f"{Bot_Nickname}为你准备了{n}张随机{tag}图片！")

    def choice_api(tag: str):
        if not tag or (tag := is_MirlKoi_tag(tag)):
            api = "MirlKoi API"
            setufunc = MirlKoi
        else:
            api = "Jitsu"
            setufunc = Anosu
        return setufunc

    if event.kwargs["group_id"]:
        if r18:
            resp.append("(r18禁止)")

    else:
        if r18:
            r18 = 1

    msg += f"{Bot_Nickname}为你准备了{N}张随机{Tag or '图片'}！\n图片取自：{api}"
    url_list = await setufunc(N, Tag)
    if url_list is None:
        return Result("text", msg + "\n连接失败，请稍等一年后重试。")
    image_list = [Result("image", url) for url in url_list if url]
    if len(image_list) == 1:
        return Result("list", [Result("text", msg), image_list[0]])

    async def result():
        yield Result("text", msg)
        for x in image_list:
            yield x

    return Result("segmented", result())


__plugin__ = plugin
