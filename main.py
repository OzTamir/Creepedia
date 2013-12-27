from flask import Flask
from WikiParse import WikiParse
from Creepedia import *

app = Flask(__name__)

exif = get_exif_data('IMG2.JPG')
lat, lon = gps_coord(exif)
articles = articles(lat, lon, 1000, 1, '')


def getTableItem(articles):
    table = '<table><tbody><tr>'
    for article in articles:
        if 'url' in article:
            parse = WikiParse(article['url'])
            picture = parse.parsePicture()
            table += '<td><img src="' + picture + '">'
            title = parse.parseTitle()
            table += '<a href="' + article['url'] + '"><h3>' + str(title) + '</h3></a></td>'
    table += '</tr><br></tbody></table><br><br>'
    return str(table)


@app.route('/')
def stock():
    return '''
	<center>
	<h1 style="font-family:sans-serif;"> Creepedia </h1>
	<hr>
	<div>
		<div>
		%s
		</div>
		<hr>
		<br><br>
		<div> 
			<img src="http://maps.googleapis.com/maps/api/streetview?size=300x300&location=%s&heading=235&sensor=false" /> 
			<img src="http://maps.googleapis.com/maps/api/staticmap?center=%s&zoom=17&size=600x300&sensor=false" />
		</div>
		<iframe src="%s" width="900px" height="300px" />
	</div>
	</center>
		''' % (str(getTableItem(articles)), str(lat) + ',' + str(lon), str(lat) + ',' + str(lon), articles[0]['url'] )


if __name__ == '__main__':
    app.run()
