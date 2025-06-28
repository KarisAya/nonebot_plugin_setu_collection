from nonebot import require, get_plugin_config
from nonebot.plugin import PluginMetadata
from clovers.config import Config as CloversConfig
from .config import Config


__plugin_meta__ = PluginMetadata(
    name="来张色图",
    description="从多个api获取色图并根据场景整合的色图插件",
    usage="来N张xx色图",
    type="application",
    config=Config,
    homepage="https://github.com/KarisAya/nonebot_plugin_setu_collection",
    supported_adapters=None,
)
IMPORT_NAME = "clovers_setu_collection"
PREFIX_LENGTH = len("setu_collection_")
CloversConfig.environ()[IMPORT_NAME] = {k[PREFIX_LENGTH:].lower(): v for k, v in get_plugin_config(Config).model_dump().items()}
require("nonebot_plugin_clovers").client.load_plugin(IMPORT_NAME)
