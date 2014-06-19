from google.appengine.ext import ndb


class User(ndb.Model):
    name = ndb.StringProperty(required=True)
    pw_hash = ndb.StringProperty(required=True)
    about = ndb.TextProperty()
    #campaigns = ndb.StructuredProperty(Campaign, repeated=True, default=None)
    btc_address = ndb.StringProperty()


class Campaign(ndb.Model):
    name = ndb.StringProperty(required=True)
    btc_address = ndb.StringProperty(required=True)
    about = ndb.TextProperty()
    amount_wanted = ndb.FloatProperty()