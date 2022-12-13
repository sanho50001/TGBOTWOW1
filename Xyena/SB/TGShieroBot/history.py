import sqlite3
import datetime
db = sqlite3.connect('TelegramDB.db')
sql = db.cursor()

class DataBase:

    def __init__(self, user_id):
        self.User_id = user_id
        self.request = ''
        self.datetime = datetime.datetime.now().strftime('Date: %Y %m %d Time: %H:%M:%S')
        self.hostels = ''


    def create_db(self):

        sql.execute(f"""CREATE TABLE IF NOT EXISTS users (
            user_id TEXT,
            requests TEXT,
            datatime TEXT,
            hostels TEXT
            )""")
        db.commit()

        pass

    def add_in_base(self):

        sql.execute(f"""SELECT user_id FROM users WHERE user_id = {self.User_id}""")
        if sql.fetchone() is None:
            sql.execute(f'INSERT INTO users VALUES (?,?,?,?)', (self.User_id, self.request, self.datetime, self.hostels))
            db.commit()
        else:
            self.upgrade_db_request(request=self.request)
            self.upgrade_db_hostels(hostel=self.hostels)

    def upgrade_db_request(self, request):
        sql.execute(f"""UPDATE users SET {request} = WHERE {self.request} """)
        db.commit()

    def upgrade_db_hostels(self, hostel):
        sql.execute(f"""UPDATE users SET {hostel} = WHERE {self.hostels} """)
        db.commit()

    def read_in_base(self):
        for _ in sql.execute('SELECT * FROM users'):
            print(_)

    def delete_db(self, user_id):
        sql.execute(f"DELETE FROM users WHERE user_id = '{user_id}'")
        db.commit()

    def predel(self):
        for _ in sql.execute('SELECT * FROM users'):
            self.delete_db(user_id=_[0])

    def set_request(self, request):
        self.request = request

    def set_hostels(self, hostels):
        self.hostels = hostels



    # def get_request(self):
    #     return self.request
    #
    # def get_hostels(self):
    #     return self.hostels
#
#
#
# testdb = DataBase('3312')
# testdb.create_db()
# testdb.set_hostels('dsadas')
# testdb.set_request('TaeasaeS')
# testdb.add_in_base()
# #
# # testdb.predel()
# testdb.read_in_base()
# # testdb.delete_db()
