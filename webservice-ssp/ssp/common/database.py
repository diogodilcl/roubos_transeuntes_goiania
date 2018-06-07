# from contextlib import contextmanager
#
# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker
#
# from config import SQLALCHEMY_DATABASE_URI
#
#
# class Database:
#
#     @contextmanager
#     def db_connection(self):
#         connect_string = SQLALCHEMY_DATABASE_URI
#
#         engine = create_engine(connect_string, echo=False, encoding='utf8mb4')
#         connection = engine.connect()
#
#         yield connection
#
#         connection.close()
#
#     @contextmanager
#     def db_session(self):
#         connect_string = SQLALCHEMY_DATABASE_URI
#
#         engine = create_engine(connect_string, echo=False)
#         connection = engine.connect()
#         session = scoped_session(sessionmaker(autocommit=False, autoflush=True, bind=engine))()
#
#         yield session
#
#         session.close()
#         connection.close()
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
