from petascope_cache import db
from datetime import datetime



class Cached_WCPS(db.Model):
    hash = db.Column(db.String(32), primary_key=True)
    result = db.Column(db.String(1000))
    mime = db.Column(db.String(100))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, _hash, result, mime, date=None):
        self.hash = _hash
        self.result = result
        self.mime = mime
        self.date_added = date

    def __repr__(self):
        return'<Cached_WCPS %s : %s mime-type: %s datetime : %s>' % (self.hash, self.result, self.mime, self.date_added)
