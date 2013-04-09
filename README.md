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

INSTALL
=======

1. Get a virtualenv running.
2. Install dependencies: ```pip install -U -r requirements.txt```
3. Copy ```settings.py-dist``` to ```settings.py``` and tweak the settings within
3. Start the SMTPd: ```twistd -y smtpd.py --logfile=smtpd.log```
4. Deploy the Flask-powered app.py, [see their deployment docs](http://flask.pocoo.org/docs/deploying/wsgi-standalone/)
5. Forward your port 25/tcp to your chosen ```SMTPD_PORT```, like so: ```iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 25 -j REDIRECT --to-port 2500```
6. Set a MX DNS record for your domain(s)

...and that's it. If you need help, you'll find me on [irc.hackint.org](irc://irc.hackint.org/). Just ```/msg zakx```.
