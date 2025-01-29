from pydantic import BaseModel


class Config(BaseModel):
    nonebot_plugin_setu_collection_save_image: bool = True
    """是否保存从api获取的图片"""
    nonebot_plugin_setu_collection_path: str = "./data/setu_collection"
    """主路径"""
    nonebot_plugin_setu_collection_private_setu_limit: bool = False
    """私聊图片限制"""
    nonebot_plugin_setu_collection_private_setu_api: str = "Lolicon API"
    """私聊使用的图片api"""
    nonebot_plugin_setu_collection_public_setu_limit: bool = True
    """群聊图片限制（别关）"""
    nonebot_plugin_setu_collection_public_setu_api: str = "Jitsu/MirlKoi API"
    """群聊使用的图片api"""
