import hashlib
import random
import quopri
import StringIO
from string import letters
from secrets import secret_string
import hmac
import time
from hashlib import sha1


# password hash
def make_salt(length=10):
    return ''.join(random.choice(letters) for x in xrange(length))


def make_pw_hash(name, pw, salt=None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)


def valid_pw(name, password, h):
    salt = h.split(',')[0]
    return h == make_pw_hash(name, password, salt)


# FORM VALIDATORS
import re
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")


def valid_username(username):
    return username and USER_RE.match(username)


def valid_password(password):
    return password and PASS_RE.match(password)


def valid_email(email):
    return not email or EMAIL_RE.match(email)


def encodestring(instring, tabs=0):
    outfile = StringIO.StringIO()
    quopri.encode(StringIO.StringIO(instring), outfile, tabs)
    return outfile.getvalue()


def decodestring(instring):
    outfile = StringIO.StringIO()
    quopri.decode(StringIO.StringIO(instring), outfile)
    return outfile.getvalue()


# auth token
def hmac_hash_sha1(key, message):
    return hmac.new(key=key, msg=message, digestmod=sha1).hexdigest()


def generate_token(userid, secret=secret_string, time_valid=864000):
    expiration_time = int(time.time()) + time_valid  # that's time in seconds. time_valid by default is 864000s (10 days)
    if userid and secret:
        message = '%s---%s' % (userid, expiration_time)
        hmac_hash = hmac_hash_sha1(key=secret, message=message)
        return '%s|%s,%s' % (userid, hmac_hash, expiration_time)


def validate_token(token, secret):
    if token and secret:
        expiration_time = token.split(',')[1]
        current_time = int(time.time())
        if current_time < expiration_time:
            userid = token.split('|')[0]
            other_part = token.split('|')[1]
            hmac_hash = other_part.split(',')[0]
            message = '%s---%s' % (userid, expiration_time)
            if hmac_hash == hmac_hash_sha1(key=secret, message=message):
                return True
            else:
                return False
        else:
            return False
    else:
        return False