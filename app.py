import datetime

import flask
import wikipedia
import requests

import PyRSS2Gen
import StringIO

wikipedia.set_lang("de")

app = flask.Flask(__name__)


def gen_rss(shows):
    items = []

    for show in shows:
        items.append(PyRSS2Gen.RSSItem(
             title = show['title'],
             link = "http://www.example.com",
             description = show['channel'],
             guid = PyRSS2Gen.Guid(show['guid']),
             pubDate = show['start']))

    rss = PyRSS2Gen.RSS2(
        title = "TV-Jetzt",
        link = "http://tvfeed.herokuapp.com",
        description = "Jetzt",
        lastBuildDate = datetime.datetime.now(),
        items = items)
    #output = StringIO.StringIO()
    #rss.write_xml(output)
    return rss.to_xml(encoding = "utf-8")

def get_prev_shows():
    now = datetime.datetime.utcnow()
    date =  now.strftime('%Y%m%dT%H%M%SZ')
    url = 'http://hackathon.lab.watchmi.tv/api/example.com/broadcasts/prevnext/'+date+',-1,1/field/tit/field/time/field/stit/field/mgnr/field/chanlong/sort/chid/sort/time_start'
    print url
    return requests.get(url).json()['results']

@app.route("/feed")
def index():
    shows = []
    for show in get_prev_shows():
        parsed = {}
        parsed['channel'] = show['channelNameLong']
        parsed['title'] = show['epgData']['tit'][0]['value']
        parsed['start'] = datetime.datetime.fromtimestamp(show['epgData']['time']['strt']/1000)
        parsed['end'] = datetime.datetime.fromtimestamp(show['epgData']['time']['end']/1000)
        parsed['guid'] = show['epgData']['pid']
        shows.append(parsed)

    feed = gen_rss(shows)
    #return flask.render_template('index.html', shows=shows)
    return flask.Response(feed, mimetype='text/xml')

@app.route("/index")
def person(name):
    ['<a href="/feed"> Feed </a>']

@app.route("/unsubscribe/<token>")
def unsubscribe(token):
    return "Hello World!"

if __name__ == "__main__":
    app.run(debug=True)