import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from models.base_model import Base, BaseModel
from models.city import City
from models.state import State


USER = os.getenv('HBNB_MYSQL_USER')
PASSWORD = os.getenv('HBNB_MYSQL_PWD')
HOST = os.getenv('HBNB_MYSQL_HOST')
DB = os.getenv('HBNB_MYSQL_DB')


class DBStorage:
    __engine = None
    __session = None
    
    def __init__(self):
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(USER, PASSWORD,
                                              HOST, DB),
                                      pool_pre_ping=True)
        if 'test' in sys.argv:
            Base.metadata.drop_all(self.__engine)
    
    def all(self, cls=None):        
        if cls is None:
            objs = self.__session.query(State).all()
            objs.extend(self.__session.query(City).all())
            # objs.extend(self.__session.query(User).all())
            # objs.extend(self.__session.query(Place).all())
            # objs.extend(self.__session.query(Review).all())
            # objs.extend(self.__session.query(Amenity).all())
        else:
            if type(cls) == str:
                cls = eval(cls)
            objs = self.__session.query(cls)
        return {"{}.{}".format(type(obj).__name__, obj.id): obj for obj in objs}
    
    def new(self, obj):
        self.__session.add(obj)
    
    def save(self):
        self.__session.commit()
    
    def delete(self, obj=None):
        if obj:
            self.__session.delete(obj)
    
    def reload(self):
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
    
    def close(self):
        self.__session.close()