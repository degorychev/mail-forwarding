import imaplib
import email
import base64

class Mail:

    def __init__(self, mail, password):
        self.mail = imaplib.IMAP4_SSL('imap.'+mail.split('@')[1])
        self.mail.login(mail, password)
        self.mail.select()
        self.adress = mail

    def _select(self):
        result = self.mail.select()
        while result[0] != 'OK':
            result = self.mail.select()

    def get_adress(self):
        return self.adress

    def get_last_uid(self):
        self._select()
        result, data = self.mail.uid('search', None, "ALL")  # Выполняет поиск и возвращает UID писем.
        return data[0].split()[-1]

    def get_latest_raw(self):
        self._select()
        result, data = self.mail.uid('fetch', self.get_last_uid(), '(RFC822)')
        raw_email = data[0][1]
        return raw_email

    def get_latest(self):
        self.mail.select()
        mail = email.message_from_bytes(self.get_latest_raw())

        maintype = mail.get_content_maintype()

        _text = []

        if maintype == 'multipart':
            for part in mail.get_payload():
                if part.get_content_maintype() == 'text':
                    _text.append(part.get_payload())
        elif maintype == 'text':
            _text.append(mail.get_payload())

        text = []

        for i in _text:
            try:
                text.append(base64.decodebytes(i.encode()).decode('utf-8'))
            except:
                continue
        if len(text) != 0:
            return text[0]
        else:
            return 'Вам пришло не текстовое сообщение.'