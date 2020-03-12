from vk_api import vk_api, VkUpload
from config.conf import Config
import app.models.models_DB as Models
from app import menus
from app.controller import Controller
from app.app import App

vk = vk_api.VkApi(token=Config.VK_TOKEN)
print('[*] Авторизация с ВКонтакте... ', end='')
vk._auth_token()
vk_upload = VkUpload(vk)
print('Успешно')


app = App(vk, vk_upload, menus.MenuTree(), controller=Controller(), models=Models)


if __name__ == '__main__':
    app.run()
