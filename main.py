from vk_api import vk_api, VkUpload
from app import menues
from app.app import App
from config.conf import Config

vk = vk_api.VkApi(token=Config.VK_TOKEN)
print('[*] Авторизация с ВКонтакте... ', end='')
vk._auth_token()
vk_upload = VkUpload(vk)
print('Успешно')
app = App(vk, vk_upload, menues.MenuTree())

if __name__ == '__main__':
    import app.models.models as orm_models
    import app.seeds.seeds as seeds

    app.run()
