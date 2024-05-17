#!/usr/bin/python3
"""
the class DBStorage
"""

import models
from models.base_model import BaseModel, Base
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from models.amenity import Amenity
from models.review import Review
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {"State": State, "City": City, "Place": Place,
           "User": User, "Amenity": Amenity, "Review": Review}


class DBStorage:
    """ interacts with the MySQL database """
    __engine = None
    __session = None

    def __init__(self):
        """ instatiate a DBStorage object """
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}:{}/{}'
                                      .format(getenv(HBNB_MYSQL_USER),
                                              getenv(HBNB_MYSQL_PWD),
                                              getenv(HBNB_MYSQL_HOST),
                                              getenv(HBNB_MYSQL_PORT),
                                              getenv(HBNB_MYSQL_DB)),
                                      pool_pre_ping=True)
        if getenv('HBNB_ENV') == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ query on the current database session """
        objs = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        """ add the object to the current database session """
        self.__session.add(obj)

    def save(self):
        """ commit all the changes of the current database session """
        self.__session.commit()

    def delete(self, obj=None):
        """ delete from the current database session obj if not None """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """ reloads data from the database """
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """ call remove() method on the private session attribute """
        self.__session.remove()
