class Settings:

    def __init__(self):
        self.owner = ''
        self.admin = ''
        self.moderator = ''
        self.connect = ''

    def set_admin(self, text):
        self.admin = text

    def set_moderator(self, text):
        self.moderator = text

    def set_connect(self, text):
        self.connect = text

    def get_admin(self):
        return self.admin

    def get_moderator(self):
        return self.moderator

    def get_connect(self):
        return self.connect

