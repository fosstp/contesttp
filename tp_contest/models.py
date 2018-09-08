'''定義資料庫 ORM'''
import hashlib
import datetime
from sqlalchemy import ForeignKey, String, Integer, Text, DateTime, Column, Table
from sqlalchemy.orm import relationship, backref
from pyramid_sqlalchemy import BaseObject


class BaseAccount:
    '''管理者帳號、學校帳號的 base class'''

    id = Column(Integer, primary_key=True)

    # 學校名稱
    name = Column(String(100), unique=True)

    # 學校帳號，國小是 a + 學校代碼（例如a300000），國中是 b + 學校代碼（例如b300000）
    account = Column(String(100), unique=True)

    # 電子郵件信箱
    email = Column(String(100), nullable=False)

    # 密碼，外界應該靠 property 存取此欄位
    _password = Column(String(100), nullable=False)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        '''加密明碼'''
        self.password = hashlib.sha512(
            value.encode('utf-8')).hexdigest()

class Manager(BaseAccount, BaseObject):
    '''管理者帳號'''

    __tablename__ = 'managers'

    # 帳號等級，0 代表最高管理者，1 代表活動管理者
    type = Column(Integer)

    competition = relationship('Competition', backref='manager')

    competition_news = relationship('CompetitionNews', backref='manager')

schools_competition_table = Table('schools_competition', BaseObject.metadata,
    Column('school_id', Integer, ForeignKey('schools.id')),
    Column('competition_id', Integer, ForeignKey('competition.id'))
)

class School(BaseAccount, BaseObject):
    '''學校帳號'''

    __tablename__ = 'schools'

    # 學程，1 是幼兒園， 2 是國小， 3 是國中
    type = Column(Integer)

    competition = relationship("Competition", secondary=schools_competition_table, back_populates="schools")

class Competition(BaseObject):
    '''比賽'''

    __tablename__ = 'competition'

    id = Column(Integer, primary_key=True)
    
    # 比賽名稱
    name = Column(String(100))

    # 報名開始時間
    begin_signup_datetime = Column(DateTime, nullable=False)

    # 報名結束時間
    end_signup_datetime = Column(DateTime, nullable=False)

    # 管理者
    manager_id = Column(Integer, ForeignKey('managers.id'))

    schools = relationship("School", secondary=schools_competition_table, back_populates="competition")

    sign_up = relationship('CompetitionSignUp', backref='competition')

    news = relationship('CompetitionNews', backref='competition')

class CompetitionSignUp(BaseObject):
    '''報名特定活動的紀錄'''

    __tablename__ = 'competition_sign_up'

    id = Column(Integer, primary_key=True)

    # 學生名字
    student_name = Column(String(100))

    # 學生班級
    student_class = Column(String(100))

    # 指導老師 1
    instructor1 = Column(String(100))

    # 指導老師 2
    instructor2 = Column(String(100))

    # 報名時間
    signup_datetime = Column(DateTime, nullable=False, default=datetime.datetime.now)

    # 歸屬哪一個競賽
    competition_id = Column(Integer, ForeignKey('competition.id'))

class CompetitionNews(BaseObject):
    '''報名活動的消息公佈'''

    __tablename__ = 'competition_news'

    id = Column(Integer, primary_key=True)

    # 最新消息標題
    title = Column(String(100))

    # 最新消息內容
    content = Column(Text)

    # 發佈時間
    publication_date = Column(DateTime, nullable=False, default=datetime.datetime.now)

    # 歸屬哪一個競賽
    competition_id = Column(Integer, ForeignKey('competition.id'))

    # 作者
    manager = Column(Integer, ForeignKey('managers.id'))