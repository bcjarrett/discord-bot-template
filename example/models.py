import peewee

from database import BaseModel


class LastResponse(BaseModel):
    text = peewee.CharField(null=False)
    user_id = peewee.BigIntegerField(null=False)
