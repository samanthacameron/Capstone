from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import *


Base = declarative_base()


class School(Base):
    __tablename__ = 'school'
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    grade = Column(String(50), nullable=True)
    


class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    first = Column(String(50), nullable = False)
    last = Column(String(50), nullable = False)
    email = Column(String(50), nullable = True)
    school_id = Column(Integer, ForeignKey('school.id'), nullable=True)
    courses = Column(String(1000))


class Teacher(Base):
    __tablename__ = 'teacher'
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    first = Column(String(50), nullable = False)
    email = Column(String(50), nullable = True)
    last = Column(String(50), nullable = False)
    school_id = Column(Integer, ForeignKey('school.id'), nullable=True)
    courses = Column(String(1000))

class Textbook(Base):
    __tablename__ = 'textbook'
    id = Column(Integer, primary_key=True)
    isbn = Column(String(50), nullable=False)
    title = Column(String(50), nullable = False)
    author = Column(String(50), nullable = False)
    edition = Column(String(50), nullable = False)
    school_id = Column(Integer, ForeignKey('school.id'), nullable=True)
    
class Courses(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    des = Column(String(500), nullable=True)
    subject = Column(String(50), nullable=False)
    number = Column(String(50), nullable = False)
    name = Column(String(50), nullable = True)
    teacher_id = Column(Integer, ForeignKey('teacher.id'), nullable=True)
    school_id = Column(Integer, ForeignKey('school.id'), nullable=True)
    textbook_id = Column(Integer, ForeignKey('textbook.id'), nullable=True)



# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.

user = '<username>'
password = '<password>'
database_host = '127.0.0.1'
engine = create_engine(
    'mysql+mysqlconnector://{}:{}@{}/capstone'.format(user, password, database_host))
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
metadata = MetaData()

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)
