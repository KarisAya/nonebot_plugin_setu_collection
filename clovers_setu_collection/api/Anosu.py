import httpx
import json


async def Anosu(N: int = 1, Tag: str = ""):
    async with httpx.AsyncClient() as client:
        url = f"https://image.anosu.top/pixiv/json?num={N}&keyword={Tag}"
        resp = await client.get(url)
    if resp.status_code != 200:
        return

    resp = resp.text
    resp = "".join(x for x in resp if x.isprintable())
    anosu_list = json.loads(resp)
    if not anosu_list:
        return []
    return [x["url"] for x in anosu_list]
