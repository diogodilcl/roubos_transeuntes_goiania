import os

import yaml

APP_ENV = 'development'
ROOT = os.path.dirname(os.path.abspath(__file__))


def load_config_file(name: str):
    return yaml.load(open(ROOT + "/ssp/common/{}.yml".format(name), 'r'))[APP_ENV]


class Config:
    DATABASE = load_config_file('database')
    SQLALCHEMY_DATABASE_URI = "{}://{}:{}@{}/{}?charset=utf8mb4".format("mysql+pymysql", DATABASE['user'],
                                                                        DATABASE['password'],
                                                                        DATABASE['host'], DATABASE['database'])
    SQLALCHEMY_TRACK_MODIFICATIONS = False
