from sqlobject import AND

from . import models


def get_or_create_domain(name):
	try:
		domain = models.Domain.select(models.Domain.q.name == name)[0]
	except IndexError:
		domain = models.Domain(name=name)
	return domain


def get_or_create_user(name, domain):
	try:
		user = models.User.select(AND(models.User.q.name == name, models.User.q.domain == domain))[0]
	except IndexError:
		user = models.User(name=name, domain=domain)
	return user
