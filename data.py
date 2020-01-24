import sqlite3

class Data:

    def __init__(self):
        self.data = sqlite3.connect('data.sqlite', check_same_thread=False)
        self.data_cursor = self.data.cursor()
        self.data_cursor.execute('create table if not exists People(id, mail, password, luid)')

    def get_all(self):
        self.data_cursor.execute('select mail, password, luid from People')
        return self.data_cursor.fetchall()

    def get_all_id(self):
        self.data_cursor.execute('select id from People')
        return self.data_cursor.fetchall()

    def get_all_mail_with_password(self):
        self.data_cursor.execute('select mail, password from People')
        return self.data_cursor.fetchall()

    def get_id_by_mail(self, mail):
        self.data_cursor.execute('select id from People where mail=?', (mail,))
        return self.data_cursor.fetchall()

    def get_mail_by_id(self, id):
        self.data_cursor.execute('select mail from People where id=?', (id,))
        return self.data_cursor.fetchall()

    def is_exist(self, mail):
        if self.get_id_by_mail(mail):
            return True
        return False

    def set_luid(self, mail, luid):
        self.data_cursor.execute('update People set luid=? where mail=?', (luid, mail))
        self.data.commit()

    def get_luid(self, mail):
        self.data_cursor.execute('select luid from People where mail=?', (mail,))
        return self.data_cursor.fetchall()[0][0]

    def add(self, id, mail, password):
        self.data_cursor.execute('insert into People values(?, ?, ?, ?)', (id, mail, password, -1))
        self.data.commit()

    def dell(self, mail):
        self.data_cursor.execute('delete from People where mail=?', (mail,))
        self.data.commit()

    def __del__(self):
        self.data.commit()
        self.data.close()
        print('Работа базы данных успешно завершена.')
