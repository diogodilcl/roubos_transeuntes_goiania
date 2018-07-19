from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

# engine = create_engine('postgresql://dbuser:dbpassword@localhost:5432/sqlalchemy-orm-tutorial')
# # use session_factory() to get a new Session
# _SessionFactory = sessionmaker(bind=engine)
# def session_factory():
#     Base.metadata.create_all(engine)
#     return _SessionFactory()

# Base = declarative_base()

DATABASE_CONNECTION = "{}://{}:{}@{}/{}?charset=utf8mb4".format("mysql+pymysql", "root",
                                                                "xpto1234",
                                                                "localhost", "ssp_go")


class Database:

    @contextmanager
    def db_connection(self):
        connect_string = DATABASE_CONNECTION

        engine = create_engine(connect_string, echo=False, encoding='utf8mb4')
        connection = engine.connect()

        yield connection

        connection.close()

    @contextmanager
    def db_session(self):
        connect_string = DATABASE_CONNECTION

        engine = create_engine(connect_string, echo=False)
        connection = engine.connect()
        session = scoped_session(sessionmaker(autocommit=False, autoflush=True, bind=engine))()

        yield session

        session.close()
        connection.close()
