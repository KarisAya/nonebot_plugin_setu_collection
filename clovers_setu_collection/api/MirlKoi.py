import httpx
import json

MirlKoi_list = {}
MirlKoi_list["iw233"] = []
MirlKoi_list["top"] = []
MirlKoi_list["yin"] = []
MirlKoi_list["cat"] = []
MirlKoi_list["xing"] = []
MirlKoi_list["mp"] = []
MirlKoi_list["pc"] = []

MirlKoi_tag = {
    "涩图 随机图片 随机壁纸": "iw233",
    "推荐": "top",
    "白毛 白发 银发": "yin",
    "兽耳 猫耳 猫娘": "cat",
    "星空 夜空 星空壁纸 夜空壁纸": "xing",
    "壁纸 竖屏壁纸 手机壁纸": "mp",
    "电脑壁纸 横屏壁纸": "pc",
}

tag_dict = {}
for key in MirlKoi_tag:
    value = MirlKoi_tag[key]
    tag_dict[value] = key.split()[0]


def is_MirlKoi_tag(Tag: str = ""):
    for x in MirlKoi_tag.keys():
        if Tag in x.split():
            return MirlKoi_tag[x]
        else:
            continue
    else:
        return None


async def MirlKoi(N: int = 1, Tag: str = None):
    tag = tag_dict.get(Tag, "iw233")
    async with httpx.AsyncClient() as client:
        url = f"https://dev.iw233.cn/api.php?sort={tag}&type=json&num=100"
        resp = await client.get(url)

    if resp.status_code != 200:
        return

    resp = resp.text
    resp = "".join(x for x in resp if x.isprintable())
    MirlKoi_list[tag] += json.loads(resp)["pic"]

    image_list = MirlKoi_list[tag][:N]
    MirlKoi_list[tag] = MirlKoi_list[tag][N:]
    return image_list
