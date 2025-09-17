from app.db.connection import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship



class Users(Base):
    __tablename__ = "users"
    
    id = Column("id", String, primary_key=True)
    name = Column("name", String)
    age = Column("age", Integer)
    score = Column("score", Integer)
    active = Column("active", Boolean)
    country = Column("country", String)
    team = relationship("Team", back_populates="users")
    logs = relationship("Logs", back_populates="users")


class Team(Base):
    __tablename__ = 'team'

    id = Column("id", Integer, autoincrement=True, primary_key=True)
    name = Column("name", String)
    leader = Column("leader", Boolean)
    users = relationship("Users", back_populates="team")
    user_id = Column("user_id", ForeignKey("users.id"))
    projects = relationship("Projects", back_populates="team")

class Projects(Base):
    __tablename__ = 'projects'

    id = Column("id", Integer, autoincrement=True, primary_key=True)
    name = Column("name", String)
    completed = Column("completed", Boolean)
    user_id = Column("user_id", ForeignKey("team.user_id"))
    team = relationship("Team", back_populates="projects")

class Logs(Base):
    __tablename__ = 'logs'

    id = Column("id", Integer, autoincrement=True, primary_key=True)
    date = Column("date", Date)
    action = Column("action", String)
    users = relationship("Users", back_populates="logs")
    user_id = Column("user_id", ForeignKey("users.id"))