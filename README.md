tempmail
========

**tempmail** is a temporary e-mail address provider (including SMTP server and web frontend).
Basically your own Mailinator -- only that it's not blocked everywhere.

Components:
* Small SMTPd (python/Twisted), *smtpd.py*
* Web Frontend (python/Flask), *app.py*

Notable features:
* no-frills plaintext message display
* no registration neccessary
* multi-domain support
* new mails can be deleted by anyone for 10 minutes
* decoding MIME-encoded text

You can see a demo installation at http://tm.zakx.de/.
