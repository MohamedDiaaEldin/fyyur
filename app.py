#----------------------------------------------------------------------------#
# Imports
# author -; mohamed diaa
#----------------------------------------------------------------------------#

import json
from operator import add
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import Pagination, SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from sqlalchemy.orm import backref, lazyload
from forms import *
from config import SQLALCHEMY_DATABASE_URI
from flask_migrate import Migrate, current
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
migrate = Migrate(app=app, db=db)
#---------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
from models import Artist, Venue, Genre, Show


# TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#
##


# delete notes --> i should delete a record first from genres and shows if there
# then delete the artist or venue


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime


def add_to_dic(venue, dic):
    city = venue.city + ", " + venue.state
    if city not in dic:
        dic[city] = [venue]
    else:
        dic[city].append(venue)


#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
    return render_template('pages/home.html')


@app.route('/venues')
def venues():
    # TODO: replace with real venues data.
    #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
    data = []
    cities = {}
    for venue in Venue.query.all():
        add_to_dic(venue, cities)

    for city in cities.keys():
        current_city = {}
        city_and_state = city.split(',')
        current_city["city"] = city_and_state[0]
        current_city["state"] = city_and_state[1]
        current_venues = []
        for venue in cities[city]:
            current_venues.append(
                {
                    "id": venue.id,
                    "name": venue.name,
                    "num_upcoming_shows": 1  # static for now
                }
            )
        current_city["venues"] = current_venues
        data.append(current_city)
    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    response = {
        "count": 1,
        "data": [{
            "id": 2,
            "name": "The Dueling Pianos Bar",
            "num_upcoming_shows": 0,
        }]
    }
    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    venue = Venue.query.get(venue_id)
    print(venue)
    data = {
        "id": venue.id,
        "name": venue.name,
        "genres": Genre.query.filter_by(venue_id=venue_id),
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website_link,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link,
        "past_shows": [{
            "artist_id": 4,
            "artist_name": "Guns N Petals",
            "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
            "start_time": "2019-05-21T21:30:00.000Z"
        }],
        "upcoming_shows": [],
        "past_shows_count": 1,
        "upcoming_shows_count": 0,
    }
    return render_template('pages/show_venue.html', venue=data)


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    is_added_venue = False
    try:
        datetime.now()
        name = request.form['name']
        city = request.form['city']
        state = request.form['state']
        address = request.form['address']
        phone = request.form['phone']
        image_link = request.form['image_link']
        genres = request.form.getlist('genres')
        facebook_link = request.form['facebook_link']
        website_link = request.form['website_link']
        seeking_talent = False
        if 'seeking_talent' in request.form:
            seeking_talent = True
        seeking_description = request.form['seeking_description']

        venue = Venue(name=name, city=city, state=state,
                      address=address, phone=phone, image_link=image_link, facebook_link=facebook_link,
                      website_link=website_link, seeking_talent=seeking_talent,
                      seeking_description=seeking_description,)
        db.session.add(venue)
        db.session.commit()
        is_added_venue = True
        venue_id = venue.id
        for genre in genres:
            db.session.add(Genre(name=genre, venue_id=venue_id))
            db.session.commit()
        flash('Venue ' + name + ' was successfully listed!')
    except:
        db.session.rollback()
        if is_added_venue:
            Venue.query.filter_by(id=venue_id).delete()
            db.session.commit()
        print('error happend')
        flash('Venue ' + name + ' was NOT added :(')
    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return None


@app.route('/artists')
def artists():
    data = db.session.query(Artist.id, Artist.name)
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    response = {
        "count": 1,
        "data": [{
            "id": 4,
            "name": "Guns N Petals",
            "num_upcoming_shows": 0,
        }]
    }
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):

    print('artist with id------------->', artist_id)

    artist = Artist.query.get(artist_id)
    data = {
        "id": artist.id,
        "name": artist.name,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website": artist.website_link,
        "facebook_link": artist.facebook_link,
        "seeking_venue": artist.seeking_venue,
        "seeking_description": artist.seeking_venue_description,
        "image_link": artist.image_link,
        "genres": Genre.query.filter_by(artist_id=artist_id),

        "past_shows": [{
            "venue_id": 1,
            "venue_name": "The Musical Hop",
            "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
            "start_time": "2019-05-21T21:30:00.000Z"
        }],
        "upcoming_shows": [],
        "past_shows_count": 1,
        "upcoming_shows_count": 0,
    }
    return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = Artist.query.get(artist_id)

    if artist: 
        form.name.data = artist.name
        form.city.data = artist.city
        form.state.data = artist.state
        form.phone.data = artist.phone
        form.facebook_link.data = artist.facebook_link
        form.image_link.data = artist.image_link
        form.website_link.data = artist.website_link
        form.seeking_venue.data = artist.seeking_venue
        form.seeking_description.data = artist.seeking_venue_description        
        form.genres.data = Genre.query.filter_by(artist_id=artist_id)
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    try:        
        artist = Artist.query.get(artist_id)
        artist.name = request.form['name']
        artist.city = request.form['city']
        artist.state = request.form['state']
        artist.phone = request.form['phone']
        artist.image_link = request.form['image_link']
        artist.facebook_link = request.form['facebook_link']
        artist.website_link = request.form['website_link']
        artist.seeking_venue = True if 'seeking_venue' in request.form else False 
        artist.seeking_description = request.form['seeking_description']
        # update genres
        db.session.commit()
        print("singer updated")
        Genre.query.filter_by(artist_id=artist_id).delete()
        for genre in request.form.getlist('genres'):
            db.session.add(Genre(name=genre, artist_id=artist_id))            
            db.session.commit()            
    except:
        db.session.rollback()
        print('error happend while updating artist')        
    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = Venue.query.get(venue_id)
    if venue :
        form.name.data = venue.name
        form.city.data = venue.city
        form.state.data = venue.state
        form.phone.data = venue.phone
        form.facebook_link.data = venue.facebook_link
        form.image_link.data = venue.image_link
        form.website_link.data = venue.website_link
        form.seeking_talent.data = venue.seeking_talent
        form.seeking_description.data = venue.seeking_description        
        form.genres.data = Genre.query.filter_by(venue_id=venue_id)
    # TODO: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    try:
        venue = Venue.query.get(venue_id)
        venue.name = request.form['name']
        venue.city = request.form['city']
        venue.state = request.form['state']
        venue.address = request.form['address']
        venue.phone = request.form['phone']
        venue.facebook_link = request.form['facebook_link']
        venue.website_link = request.form['website_link']
        venue.seeking_talent =  True if 'seeking_talent' in request.form else False 
        venue.seeking_description = request.form['seeking_description']
        venue.image_link = request.form['image_link']
        db.session.commit()
        ## updating genres
        Genre.query.filter_by(venue_id=venue_id).delete()
        db.session.commit()
        for genre in request.form.getlist('genres'):
            db.session.add(Genre(name=genre, venue_id=venue_id))
            db.session.commit()
    except:
        db.session.rollback()
        print('error happend while updating venue')
    return redirect(url_for('show_venue', venue_id=venue_id))


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    is_added_venue = False
    try:
        name = request.form['name']
        city = request.form['city']
        state = request.form['state']
        phone = request.form['phone']
        image_link = request.form['image_link']
        facebook_link = request.form['facebook_link']
        website_link = request.form['website_link']
        seeking_venue = False
        if 'seeking_talent' in request.form:
            seeking_venue = True
        seeking_venue_description = request.form['seeking_description']
        ##
        genres = request.form.getlist('genres')

        artist = Artist(name=name, city=city, state=state,
                        phone=phone, image_link=image_link, facebook_link=facebook_link,
                        website_link=website_link, seeking_venue=seeking_venue,
                        seeking_venue_description=seeking_venue_description,)
        db.session.add(artist)
        db.session.commit()
        is_added_venue = True
        artist_id = artist.id
        for genre in genres:
            db.session.add(Genre(name=genre, artist_id=artist_id))
            db.session.commit()
        flash('Artist ' + name + ' was successfully listed!')
    except:
        db.session.rollback()
        if is_added_venue:
            Venue.query.filter_by(id=artist_id).delete()
            db.session.commit()
            print('error happend while adding genres')
        else:
            print('error happend while adding artist')
        flash('Artist ' + name + 'was NOT added :(')
    return render_template('pages/home.html')


@app.route('/shows')
def shows():
    data = []
    shows = Show.query.all()
    for show in shows:
        data.append({
            'venue_id': show.venue_id,
            'venue_name': show.venue_name,
            'artist_id': show.artist_id,
            'artist_name': show.artist_name,
            'artist_image_link': show.artist_image_link,
            'start_time': show.start_time.strftime('%Y-%m-%d %H:%M:%S')
        })
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    try:
        artist_id = request.form['artist_id']
        venue_id = request.form['venue_id']
        start_time = request.form['start_time']

        artist = Artist.query.get(artist_id)
        artist_name = artist.name
        artist_image_link = artist.image_link
        venue_name = Venue.query.get(venue_id).name

        show = Show(venue_name=venue_name, artist_name=artist_name,
                    artist_image_link=artist_image_link, start_time=start_time, artist_id=artist_id, venue_id=venue_id)
        db.session.add(show)
        db.session.commit()
        flash('Show was successfully listed!')
    except:
        print('error will adding show to database')
        flash('Show was NOT added !')

    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
