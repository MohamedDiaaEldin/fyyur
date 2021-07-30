
from app import db 

class Venue(db.Model):
    __tablename__ = 'venues'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=False)
    website_link = db.Column(db.String(), nullable=True)
    # seeking_talent --> Bool
    seeking_talent = db.Column(db.Boolean, nullable=False)
    # seeking_description
    seeking_description = db.Column(db.String, nullable=False)
    # image_link
    image_link = db.Column(db.String, nullable=False)
    # geners as relationship to geners table
    all_genres = db.relationship('Genre', backref='ve_genres', lazy=True)
    # pastshows as relationship to shows table
    all_shows = db.relationship('Show', backref='ve_shows', lazy=True)
    # TODO: implement any missing fields, as a database migration using Flask-Migrate

    def __repr__(self) -> str:
        return f"id: {self.id} name: {self.name} city: {self.city}"


class Artist(db.Model):
    __tablename__ = 'artists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(), nullable=False)
    state = db.Column(db.String(), nullable=False)
    phone = db.Column(db.String(), nullable=False)
    image_link = db.Column(db.String(), nullable=False)
    facebook_link = db.Column(db.String(), nullable=False)
    website_link = db.Column(db.String(), nullable=False)
    # seeking_vanue --> bool
    seeking_venue = db.Column(db.Boolean, nullable=False)
    # seeking_vanue_description
    seeking_venue_description = db.Column(db.String, nullable=False)
    # past_shows as a relationship with shows table
    all_shows = db.relationship('Show', backref='ar_shows', lazy=True)
    # genre relation ship with genres table
    all_genres = db.relationship('Genre',  backref='ar_genres', lazy=True)


class Show(db.Model):
    __tablename__ = 'shows'
    id = db.Column(db.Integer, primary_key=True)
    venue_name = db.Column(db.String(), nullable=False)
    artist_name = db.Column(db.String(), nullable=False)
    artist_image_link = db.Column(db.String(), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'))
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'))


class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey(
        'artists.id'))
    venue_id = db.Column(db.Integer, db.ForeignKey(
        'venues.id'))

    def __repr__(self):
        return f"{self.name}"