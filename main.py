from vk_api import vk_api, VkUpload
from app import menues
from app.app import App
from config.conf import Config
import app.models.models_DB as Models
from app import menus
from app.controller import Controller

vk = vk_api.VkApi(token=Config.VK_TOKEN)
print('[*] Авторизация с ВКонтакте... ', end='')
vk._auth_token()
vk_upload = VkUpload(vk)
print('Успешно')

import app.models.orm_models as models
app = App(vk, vk_upload, menues.MenuTree(), Controller, models)



if __name__ == '__main__':
    app.run()
