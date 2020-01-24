from threading import Thread
import imaplib
from mail_check import Mail
from vk_api.longpoll import VkLongPoll, VkEventType
import time

UPDATE = False

class Listen(Thread):

    def __init__(self, vk, vk_session, base):
        super().__init__()
        self.vk = vk
        self.vk_session = vk_session
        print('Подключение к vk закончено')
        self.base = base
        print('Подключение к базе данных закончена')
        self.longpoll = VkLongPoll(self.vk_session)

    def run(self):
        print('Начинаю прослушку')
        for self.event in self.longpoll.listen():
            if self.event.type == VkEventType.MESSAGE_NEW and self.event.to_me:
                self.on_command(self.event.text.split())

    def on_command(self, text):
        global UPDATE
        if len(text) == 3 and text[0] == 'mail':
            try:
                if not self.base.is_exist(text[1]):
                    Mail(text[1], text[2])
                    self.base.add(self.event.user_id, text[1], text[2])
                    print('Почта добавлена')
                    self.vk.messages.send(
                        user_id=self.event.user_id,
                        message='Ваша почта добавлена'
                    )
                    UPDATE = True
                else:
                    self.vk.messages.send(
                        user_id=self.event.user_id,
                        message='Ваша почта уже добавлена в базу'
                    )
            except imaplib.IMAP4.error:
                self.vk.messages.send(
                    user_id=self.event.user_id,
                    message='Неправильный логин или пароль'
                )
        elif len(text) == 2 and text[0] == 'delmail':
            if self.base.is_exist(text[1]):
                if self.base.get_id_by_mail(text[1])[0][0] == self.event.user_id:
                    self.base.dell(text[1])
                    self.vk.messages.send(
                        user_id=self.event.user_id,
                        message='Почта удалена'
                    )
                    UPDATE = True
                else:
                    self.vk.messages.send(
                        user_id=self.event.user_id,
                        message='Данная почта вам не принадлежит'
                    )
            else:
                self.vk.messages.send(
                    user_id=self.event.user_id,
                    message='Данной почты нет в базе'
                )

        else:
            self.vk.messages.send(
                user_id=self.event.user_id,
                message='Команда не распознана'
            )


class Checker(Thread):
    def __init__(self, vk, base):
        super().__init__()
        self.vk = vk
        self.base = base
        self.update()
        print('Поток создан. Приступаю к активации')

    def update(self):
        global UPDATE
        self.mails = []
        for mail in self.base.get_all_mail_with_password():
            self.mails.append(Mail(mail[0], mail[1]))
        UPDATE = False
        print('Внутренняя система обновлена.')

    def run(self):
        print('Запускаю проверку почты')
        while True:
            time.sleep(10)
            if UPDATE:
                self.update()
            print('Поиск начался')
            for now in self.mails:
                with Profiler():
#                    print(now.get_adress(), now.get_last_uid(), self.base.get_luid(now.get_adress()))
                    if now.get_last_uid() != self.base.get_luid(now.get_adress()):
                        print('Найдено новое сообщение')
                        print(self.base.get_id_by_mail(now.get_adress())[0][0], 'Вам новое сообщение с '+now.get_adress()+':\n'+now.get_latest())
                        self.vk.messages.send(
                            user_id=self.base.get_id_by_mail(now.get_adress())[0][0],
                            message='Вам новое сообщение с '+now.get_adress()+':\n'+now.get_latest()
                        )
                        self.base.set_luid(now.get_adress(), now.get_last_uid())

class Profiler(object):
    def __enter__(self):
        self._startTime = time.time()

    def __exit__(self, type, value, traceback):
        print("Время проверки: {:.3f} sec".format(time.time() - self._startTime))