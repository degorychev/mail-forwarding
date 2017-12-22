import vk_api
from data import Data
from bot import Listen, Checker
import time

base = Data()

token = 'b7c37d65d4a1ed55ad8695f8516f149de13e4cad215ddfb64b8d7a9771282bfd3f8acc0de034a975ba538'

vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()
print('Приступаю к созданию бота')
listen = Listen(vk, vk_session, base)
listen.start()
print('Поток с прослушкой создан')
print('Приступаю к созданию потока с проверкой почты')
check = Checker(vk, base)
check.start()
print('Поток с проверкой почты создан')
print('Бот создан')

