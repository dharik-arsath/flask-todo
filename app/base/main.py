from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.engine import create_engine
from sqlalchemy.engine import Engine


_buffer = dict()


class Base(DeclarativeBase):
    pass


def _create_engine() -> Engine:
    sql = "sqlite:///mydb.db"
    engine = create_engine(sql, echo=True)
    _buffer["engine"] = engine
    return engine


def get_engine() -> Engine:
    if "engine" not in _buffer:
        engine = _create_engine()
    else:
        engine =  _buffer["engine"]

    return engine
