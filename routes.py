from flask import Flask, render_template, request, flash, redirect, url_for
from WikiParse import WikiParse, articleParse
import Creepedia
from werkzeug import secure_filename
import os

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'JPG', 'PNG'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/creep')
def home():
    global filename
    with app.open_resource('static/uploads/' + filename) as img:
        exif = Creepedia.get_exif_data(img)
        if exif == 'IOERROR':
            return render_template('error.html')
        try:
            lat, lon = Creepedia.gps_coord(exif)
        except KeyError:
            return  render_template('error.html')
        coord = str(lat) + ',' + str(lon)
        parsedWiki = Creepedia.articles(lat, lon, 1000, 2, '')
        articles = []
        for i in range(len(parsedWiki)):
            if 'url' in parsedWiki[i]:
                articles.append(articleParse(parsedWiki[i]['url']))
        return render_template('home.html' , coord = coord, url = articles[0].url, articles = articles)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            global filename
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('home'))
    return render_template('upload.html')
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
