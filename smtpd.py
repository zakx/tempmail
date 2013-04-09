import datetime
from email.parser import Parser

from twisted.internet import defer
from twisted.mail import smtp
from twisted.mail.mail import MailService
from zope.interface import implements

from settings import BLACKLIST_ADDRESSES
from settings import BLACKLIST_HOSTS
from settings import MY_DOMAINS
from settings import SMTPD_HOST
from settings import SMTPD_PORT
from models import connect
from models import Domain
from models import Mail
from models import User
from __init__ import get_or_create_domain
from __init__ import get_or_create_user

class TempMailMessageDelivery:
	implements(smtp.IMessageDelivery)

	def receivedHeader(self, helo, origin, recipients):
		headers = "Received: from %s via %s (from %s)\r\n" % (helo[0], helo[1], origin)
		headers += "X-Date: %s\r\n" % datetime.datetime.now()
		headers += "X-HELO: %s (%s)\r\n" % (helo[0], helo[1])
		headers += "X-MAIL-FROM: %s\r\n" % origin
		for user in recipients:
			headers += "X-RCPT-TO: %s\r\n" % user
		return headers[:-2]

	def validateFrom(self, helo, origin):
		if str(origin) not in BLACKLIST_ADDRESSES and origin.domain not in BLACKLIST_HOSTS:
			return origin
		else:
			raise smtp.SMTPBadSender(origin)

	def validateTo(self, user):
		# Only accept mail for our domains -- if set. Otherwise, anything goes.
		if not MY_DOMAINS or user.dest.domain in MY_DOMAINS:
			return lambda: TempMailMessage(user)
		raise smtp.SMTPBadRcpt(user)

class TempMailMessage:
	implements(smtp.IMessage)

	def __init__(self, user):
		self.lines = []
		self.user = user

	def lineReceived(self, line):
		self.lines.append(line)

	def eomReceived(self):
		header = ""
		header_done = False
		message = ""
		for line in self.lines:
			if header_done:
				message += line + "\r\n"
				continue
			if line == "":
				header_done = True
				continue
			header += line + "\r\n"
			thisHeader = line.split(": ", 1)
		headers = Parser().parsestr(header)
		self.lines = None

		connect()
		domain = get_or_create_domain(self.user.dest.domain)
		user = get_or_create_user(self.user.dest.local, domain)
		Mail(
			user = user,
			ts = datetime.datetime.now(),
			envelopeHeloHost = self.user.helo[0],
			envelopeHeloAddress = self.user.helo[1],
			envelopeFrom = str(self.user.orig),
			envelopeTo = str(self.user.dest),
			headerFrom = headers["from"] or "",
			headerSubject = headers["subject"] or "",
			headers = header,
			body = message
			)

		return defer.succeed(None)

	def connectionLost(self):
		# There was an error, throw away the stored lines
		self.lines = None

class TempMailSMTPFactory(smtp.SMTPFactory):
	def __init__(self):
		smtp.SMTPFactory.__init__(self)
		self.protocol = smtp.ESMTP

	def buildProtocol(self, addr):
		p = smtp.SMTPFactory.buildProtocol(self, addr)
		p.delivery = TempMailMessageDelivery()
		return p

def main():
	from twisted.application import internet
	from twisted.application import service

	a = service.Application("tempmail SMTP Server")
	internet.TCPServer(SMTPD_PORT, TempMailSMTPFactory(), interface=SMTPD_HOST or "127.0.0.1").setServiceParent(a)

	return a

application = main()
