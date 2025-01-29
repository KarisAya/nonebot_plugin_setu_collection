from nonebot import get_driver, on_message, get_plugin_config
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import Bot, MessageEvent
from nonebot.plugin import PluginMetadata
from nonebot_plugin_clovers import extract_command
from clovers import Leaf
from clovers.config import config as clovers_config
from .config import Config

# nonebot_plugin_clovers 内配置了 clovers 的 logger 所以需要先导入。

from nonebot_plugin_clovers.adapters.onebot.v11 import __adapter__ as adapter

# 先注入配置，再加载插件。
# 因为模块导入机制，如果 clovers_setu_collection 被导入过则此配置会失效。

clovers_config["clovers_setu_collection"] = {k[31:]: v for k, v in get_plugin_config(Config).model_dump().items()}

from clovers_setu_collection import __plugin__ as setu_collection
from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="来张色图",
    description="从多个api获取色图并根据场景整合的色图插件",
    usage="来N张xx色图",
    type="application",
    config=Config,
    homepage="https://github.com/KarisAya/nonebot_plugin_setu_collection",
    supported_adapters={"nonebot.adapters.onebot.v11"},
)

leaf = Leaf(adapter)
leaf.plugins.append(setu_collection)
driver = get_driver()
driver.on_startup(leaf.startup)
driver.on_shutdown(leaf.shutdown)

Bot_NICKNAME = Bot_NICKNAMEs[0] if (Bot_NICKNAMEs := list(driver.config.nickname)) else "bot"


@leaf.adapter.property_method("Bot_Nickname")
async def _():
    return Bot_NICKNAME


main = on_message(priority=20, block=False)


@main.handle()
async def _(bot: Bot, event: MessageEvent, matcher: Matcher):
    if await leaf.response(extract_command(event.get_plaintext()), bot=bot, event=event):
        matcher.stop_propagation()
