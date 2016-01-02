from datetime import datetime
from pony import orm

db = orm.Database("sqlite", "dev.sqlite", create_db=True)


class Domain(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    name = orm.Required(str, unique=True)
    users = orm.Set("User")
    visible = orm.Required(bool, default=True)


class User(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    name = orm.Required(str)
    domain = orm.Required(Domain)
    mails = orm.Set("Mail")
    acceptNewMail = orm.Required(bool, default=True)
    password = orm.Optional(str)


class Mail(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    user = orm.Required(User)
    ts = orm.Required(datetime)
    envelopeHeloHost = orm.Optional(str, 128)
    envelopeHeloAddress = orm.Optional(str, 20)
    envelopeFrom = orm.Optional(str)
    headerFrom = orm.Optional(str)
    headerSubject = orm.Optional(str)
    headers = orm.Optional(orm.LongStr)
    body = orm.Optional(orm.LongStr)


db.generate_mapping(create_tables=True)
