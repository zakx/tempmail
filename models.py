from sqlobject import *

from settings import DB_URI

def connect():
	sqlhub.processConnection = connectionForURI(DB_URI)

class Domain(SQLObject):
	name = StringCol(length=64, unique=True)

class User(SQLObject):
	name = StringCol(length=64, unique=True)
	domain = ForeignKey('Domain')

class Mail(SQLObject):
	user = ForeignKey('User')
	ts = DateTimeCol()
	envelopeHeloHost = StringCol(length=128)
	envelopeHeloAddress = StringCol(length=20)
	envelopeFrom = StringCol(length=129)
	envelopeTo = StringCol()
	headerFrom = StringCol(length=255)
	headerSubject = StringCol(length=255)
	headers = StringCol()
	body = StringCol()

if __name__ == "__main__":
	connect()
	print "Creating tables..."
	Domain.createTable()
	User.createTable()
	Mail.createTable()
	print "Done."

"""
In [20]: list(Domain.select(Domain.q.name=="tm.zakx.de"))
Out[20]: [<Domain 1 name='tm.zakx.de'>]

In [21]: list(Domain.select(Domain.q.name=="tm.zakx.dess"))
Out[21]: []
"""