from ..models.model_user import User
from ..extensions.mongodbConfig import ConnectionString
from datetime import date, datetime


class UserController:
    def __init__(self):
        self._user_name = ""
        self._email = ""
        self._password = ""
        self._create_at = datetime.now()
        self._update_at = datetime.now()
        self.conn = ConnectionString("system_db", "users")

    def getUserName(self):
        return self._user_name

    def setUserName(self, name):
        self._user_name = name

    def getEmail(self):
        return self._email

    def setEmail(self, email):
        self._email = email

    def getPassword(self):
        return self._password

    def setPassword(self, password):
        self._password = password

    def getCreateAt(self):
        return self._create_at

    def setCreateAt(self, create_at):
        self._create_at = create_at

    def getUpdateAt(self):
        return self._update_at

    def setUpdateAt(self, update_at):
        self._update_at = update_at

    def create(self):
        print(self.getEmail())
        # user = User()
        # user.user_name = self.getUserName()
        # user.email = self.getEmail()
        # user.password = self.getPassword()
        # user.create_at = self.getCreateAt()

        # db_user = ConnectionString("system_db", "users")
        # db_user.collection.insert_one(user.to_dict())

    def update(self, user_session):
        user = self.user
        self.conn.collection.update_one(
            {"user_name": user_session}, {"$set": user.to_dict()}
        )

    def find_one(self, user_name):
        db = self.conn.collection.find_one({"user_name": user_name})
        return db
