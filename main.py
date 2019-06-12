from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from vk_api import vk_api, VkUpload
from vk_api import vk_api
from config.conf import Config
from app.app import app

db = Session(bind=create_engine(Config.DATABASE, echo=False))
vk = vk_api.VkApi(token=Config.VK_TOKEN)
vk._auth_token()
vk_upload = VkUpload(vk)
app = app(db, vk, vk_upload)

if __name__ == '__main__':
    app.run()
