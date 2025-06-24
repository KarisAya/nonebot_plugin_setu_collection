from nonebot import require, get_plugin_config
from nonebot.plugin import PluginMetadata
from clovers.config import Config as CloversConfig
from .config import Config

require("nonebot_plugin_clovers")
from nonebot_plugin_clovers import client as nbcc, __plugin_meta__ as nbcc_meta


__plugin_meta__ = PluginMetadata(
    name="来张色图",
    description="从多个api获取色图并根据场景整合的色图插件",
    usage="来N张xx色图",
    type="application",
    config=Config,
    homepage="https://github.com/KarisAya/nonebot_plugin_setu_collection",
    supported_adapters=nbcc_meta.supported_adapters,
)

import_name = "clovers_setu_collection"

CloversConfig.environ()[import_name] = {k.lower().lstrip("setu_collection"): v for k, v in get_plugin_config(Config).model_dump().items()}

nbcc.load_plugin(import_name)
