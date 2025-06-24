<div align="center">

<a href="https://v2.nonebot.dev/store">
  <img src="https://raw.githubusercontent.com/A-kirami/nonebot-plugin-template/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo">
</a>

<p>
  <img src="https://raw.githubusercontent.com/A-kirami/nonebot-plugin-template/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText">
</p>

# NoneBot-Plugin-SeTu-Collection

✨ 从多个 api 获取色图并根据场景整合的色图插件 ✨

[![python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![license](https://img.shields.io/github/license/KarisAya/nonebot_plugin_setu_collection.svg)](./LICENSE)
[![pypi](https://img.shields.io/pypi/v/nonebot_plugin_setu_collection.svg)](https://pypi.python.org/pypi/nonebot_plugin_setu_collection)
[![pypi download](https://img.shields.io/pypi/dm/nonebot_plugin_setu_collection)](https://pypi.python.org/pypi/nonebot_plugin_setu_collection)
<br />

[![机器人 bug 研究中心](https://img.shields.io/badge/QQ%E7%BE%A4-744751179-maroon?)](https://qm.qq.com/q/3vpD9Ypb0c)

</div>

# 安装

使用 nb-cli 安装

```bash
nb plugin install nonebot_plugin_setu_collection
```

# 配置

详见代码注释

```env
SETU_COLLECTION_SAVE_IMAGE = true
SETU_COLLECTION_PATH = "./data/setu_collection"
SETU_COLLECTION_PRIVATE_SETU_LIMIT = false
SETU_COLLECTION_PRIVATE_SETU_API = "Lolicon API"
SETU_COLLECTION_PUBLIC_SETU_LIMIT = true
SETU_COLLECTION_PUBLIC_SETU_API = "Anosu API"
SETU_COLLECTION_HTTPX_CONFIG = '{"LoliconAPI": {"proxy":"http://127.0.0.1:7897"}}'
```

# 使用文档

[插件说明](https://github.com/clovers-project/clovers-setu-collection)
