import logging
import pyclbr
from pydoc import locate

import peewee

from config import COGS, DATABASE

logger = logging.getLogger(__name__)


class BaseModel(peewee.Model):
    class Meta:
        database = peewee.SqliteDatabase(DATABASE)


def db_setup():
    """Connect to the database and create tables for each model in each cog.models file"""
    logger.info("Connecting to peewee database")
    db = peewee.SqliteDatabase(DATABASE)
    db.connect()

    models = []

    logger.info("Attaching cogs: %s", COGS)
    for cog in COGS:
        try:
            module_info = pyclbr.readmodule(f"{cog}.models")
            for i in module_info.values():
                if (
                    i.super is not None
                    and isinstance(i.super, list)
                    and "BaseModel" in i.super
                ):
                    models.append(locate(f"{cog}.models.{i.name}"))
        except ModuleNotFoundError:
            pass

    db.create_tables(models)
