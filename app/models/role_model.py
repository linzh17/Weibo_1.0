from . import Base
from .user_model import User
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship
from . import db_session
from .Permissions import Permission

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer,primary_key=True)
    name = Column(String(64),unique=True)
    permission = Column(Integer)

    users = relationship('User',uselist=False,backref='roles')
    
    def __repr__(self):
        return '<Role %s>' %(self.name)

    @staticmethod
    def insert_roles():
        roles = {
            'User':(Permission.FOLLOW | \
                Permission.COMMIT | \
                Permission.WRITE_ARTICLES,True),

            'Moderator':(Permission.FOLLOW | \
                Permission.COMMIT | \
                Permission.WRITE_ARTICLES | \
                Permission.MODERATE_COMMENTS,True),

            'Administrator':(0xff,False)
        }

        for r in roles:
            role = Role.query.filter(Role.name == 'User').first()
            if role is None:
                role = Role(name = r)
            role.permission = roles[r][0]
            role.default = roles[r][1]
            db_session.add(role)
        db_session.commit()      