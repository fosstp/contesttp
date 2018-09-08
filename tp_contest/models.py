'''定義資料庫 ORM'''
import hashlib
from sqlalchemy import ForeighKey, String, Integer, Column
from sqlalchemy.orm import relationship, backref
from pyramid_sqlalchemy import BaseObject


class BaseAccount(BaseObject):
    '''管理者帳號、學校帳號的 base class'''

    id = Column(Integer, primary_key=True)

    # 學校名稱
    name = Column(String, unique=True)

    # 學校帳號，國小是 a + 學校代碼（例如a300000），國中是 b + 學校代碼（例如b300000）
    account = Column(String, unique=True)

    # 電子郵件信箱
    email = Column(String, nullable=False)

    # 密碼，外界應該靠 property 存取此欄位
    _password = Column(String, nullable=False)

    @property
    def password(self):
        return self._password

    @property.setter
    def password(self, value):
        '''加密明碼'''
        self.password = hashlib.sha512(
            value.encode('utf-8')).hexdigest()

class Manager(BaseAccount):
    '''管理者帳號'''

    __tablename__ = 'managers'

    # 帳號等級，0 代表最高管理者，1 代表活動管理者
    type = Column(Integer)

class School(BaseAccount):
    '''學校帳號'''

    __tablename__ = 'schools'

    # 學程，1 是幼兒園， 2 是國小， 3 是國中
    type = Column(Integer)