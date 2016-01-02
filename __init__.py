from pony import orm
import models


@orm.db_session
def get_or_create_domain(name):
	try:
		domain = orm.get(d for d in models.Domain if d.name == name)
	except IndexError:
		domain = models.Domain(name=name)
		orm.commit()
	return domain


@orm.db_session
def get_or_create_user(name, domain):
	try:
		user = orm.get(u for u in models.User if u.name == name and u.domain.name == domain)
	except IndexError:
		user = models.User(name=name, domain=orm.get(d for d in models.Domain if d.name == domain))
		orm.commit()
	return user
