from flask import Flask, render_template, request, flash
from WikiParse import WikiParse, articleParse
from Creepedia import *

app = Flask(__name__)
app.secret_key = 'hackath0n'

exif = get_exif_data('IMG2.JPG')
lat, lon = gps_coord(exif)
coord = str(lat) + ',' + str(lon)
parsedWiki = articles(lat, lon, 1000, 2, '')
articles = []
for i in range(len(parsedWiki)):
    if 'url' in parsedWiki[i]:
        articles.append(articleParse(parsedWiki[i]['url']))

@app.route('/')
def home():
  return render_template('home.html' , coord = coord, url = articles[0].url, articles = articles)

if __name__ == '__main__':
    app.run(debug = True)

# str(lat) + ',' + str(lon), str(lat) + ',' + str(lon), articles[0]['url']