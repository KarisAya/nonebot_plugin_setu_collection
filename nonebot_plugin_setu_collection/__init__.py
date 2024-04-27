from nonebot.plugin import PluginMetadata
from nonebot_plugin_clovers import clovers
__plugin_meta__ = PluginMetadata(
    name="来张色图",
    description="从多个api获取色图并根据场景整合的色图插件",
    usage="来N张xx色图",
    type="application",
    homepage="https://github.com/KarisAya/nonebot_plugin_setu_collection",
    supported_adapters={"nonebot.adapters.onebot.v11"},
)
clovers.load_plugin("clovers_setu_collection")
