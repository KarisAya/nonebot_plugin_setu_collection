from pydantic import BaseModel


class Config(BaseModel):
    setu_collection_save_image: bool = True
    """是否保存从api获取的图片"""
    setu_collection_path: str = "./data/setu_collection"
    """主路径"""
    setu_collection_private_setu_limit: bool = False
    """私聊图片限制"""
    setu_collection_private_setu_api: str = "Lolicon API"
    """私聊使用的图片api"""
    setu_collection_public_setu_limit: bool = True
    """群聊图片限制（别关）"""
    setu_collection_public_setu_api: str = "Anosu API"
    """群聊使用的图片api"""
    setu_collection_httpx_config: dict = {}
