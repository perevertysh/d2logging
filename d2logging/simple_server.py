from logger import logger
from http import HTTPStatus
import env
from bottle import HTTPResponse
from bottle import HTTPError
from bottle import route, install, template
from bottle_sqlite import SQLitePlugin
from bottle import Bottle, request, redirect
import sentry_sdk
from sentry_sdk.integrations.bottle import BottleIntegration

import album

import pdb

sentry_sdk.init(dsn=env.SENTRY_DSN,
                integrations=[BottleIntegration()])

app = Bottle()

install(SQLitePlugin(dbfile='albums.sqlite3'))


@app.route("/albums/<artist>")
def albums(artist):
    albums_list = album.find(artist)
    if not albums_list:
        message = "Альбомов {} не найдено".format(artist)
        result = HTTPError(404, message)
    else:
        album_names = [album.album for album in album.get_albums()]
        result = "Список альбомов {}:<br>".format(artist)
        result += "<br>".join(album_names)
    return result


@app.route('/albums')
def albums_list():
    # pdb.set_trace()
    albums_names = sorted([" - ".join([item.artist,
                                       item.album,
                                       str(item.year),
                                       item.genre])
                           for item in album.get_albums()])
    check_name = albums_names[0].split()[0]
    result = ""
    for item in albums_names:
        if item.split()[0] != check_name:
            result += "<hr> {}".format(item)
        else:
            result += "<br> {}".format(item)
        check_name = item.split()[0]
    return result


@app.route('/albums/add', method='GET')
def add_album():
    return '''
        <form action="/albums/add" method="post">
            artist: <input name="artist" type="text" />
            genre: <input name="genre" type="text" />
            album: <input name="album" type="text" />
            year: <input name="year" type="number" />
            <input value="add album" type="submit" />
        </form>
    '''


@app.route("/albums/add", method="POST")
def create_album():
    year = int(request.forms.get("year"))
    artist = request.forms.get("artist")
    genre = request.forms.get("genre")
    album_name = request.forms.get("album")

    new_album = album.save(year, artist, genre, album_name)
    logger.info("new row was added: {} - {}".
                 format(new_album.artist, new_album.album))
    if isinstance(new_album, album.Album):
        return redirect("/albums")
    return new_album


app.run(host='localhost', port=8080)
