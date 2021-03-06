from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from .schema import *  # noqa

# Alex Martelli's 'Borg'


class DBBorg:
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state


class DBConf(DBBorg):
    pass


conf = DBConf()


def get_db_conf():
    return conf


engine = None


def init_db_conn(scopefunc=None):
    """
    Engine and session maker should be global, so there will be attached
    to Borg configuration object
    """
    conf = get_db_conf()
    global engine
    engine = create_engine(conf.DATABASE_URI)
    Session = scoped_session(sessionmaker(), scopefunc=scopefunc)
    Session.configure(bind=engine)
    from . import orm
    orm.Session = Session
    return Session


def syncdb():
    """
    Create tables if they don't exist
    """
    Base.metadata.create_all(engine)


Base = declarative_base()

# establish a constraint naming convention.
# see http://docs.sqlalchemy.org/en/latest/core/constraints.html#configuring-constraint-naming-conventions # noqa
#
Base.metadata.naming_convention = {
    "pk": "pk_%(table_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ix": "ix_%(table_name)s_%(column_0_name)s"
}
