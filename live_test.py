# from app import format_datetime
# import time
# # 2035-04-01T20:00:00.000Z
# print(time.gmtime())
from sqlalchemy.orm import defer, query
from app import db 
from models import Venue

# word = " HI "
# print(len(word.strip()))
# print(word.strip().lower())

from sqlalchemy.orm import undefer

r = db.session.query(Venue).options(defer('name')  , undefer('id')).all()
# print(r[0].name)
print(Venue.query.all())

