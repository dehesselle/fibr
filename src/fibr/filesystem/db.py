from peewee import (
    SqliteDatabase,
    Model,
    CharField,
    IntegerField,
)

db = SqliteDatabase(":memory:")


class Files(Model):
    d_name = CharField()  # canonical
    f_mtime = IntegerField()  # TODO: datetime?
    f_name = CharField()
    f_size = IntegerField()
    f_type = IntegerField()
    _row_ts = IntegerField()  # TODO: datetime?

    class Meta:
        database = db
        indexes = ((("d_name", "f_name"), True),)
