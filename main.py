from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from vk_api import vk_api, VkUpload
from vk_api import vk_api

import app.app as app_bot
from config.conf import Config

vk = vk_api.VkApi(token=Config.VK_TOKEN)
vk._auth_token()
vk_upload = VkUpload(vk)
app = app_bot.app_bot(vk, vk_upload)

if __name__ == '__main__':
    import app.models.orm_models as orm_models
    import app.seeds.seeds as seeds
    app.run()
