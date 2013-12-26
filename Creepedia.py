from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import requests

def get_exif_data(image):
    """Get embedded EXIF data from image file."""
    exiftags = {}
    try:
        img = Image.open(image)
        if hasattr( img, '_getexif' ):
            exifinfo = img._getexif()
            if exifinfo != None:
                for tag, value in exifinfo.items():
                    decoded = TAGS.get(tag, tag)
                    exiftags[decoded] = value
    except IOError:
        print 'IOERROR ' + image
    return exiftags

def get_gps_info(exif):
    gpsinfo = {}
    for key in exif['GPSInfo'].keys():
        decode = GPSTAGS.get(key,key)
        gpsinfo[decode] = exif['GPSInfo'][key]
    return  gpsinfo

def gps_coord(exif):
    lat = [float(x)/float(y) for x, y in exif['GPSInfo'][2]]
    latref = exif['GPSInfo'][1]
    lon = [float(x)/float(y) for x, y in exif['GPSInfo'][4]]
    lonref = exif['GPSInfo'][3]

    lat = lat[0] + lat[1]/60 + lat[2]/3600
    lon = lon[0] + lon[1]/60 + lon[2]/3600
    if latref == 'S':
        lat = -lat
    if lonref == 'W':
        lon = -lon
    return  lat, lon

def articles(lat, lon, radius, limit, type_):
    """
    Returns nearby Wikipedia articles sorted by distance.
    """

    BASE_URL = "http://api.wikilocation.org/"

    articles = []
    payload = {
        "lat": lat,
        "lng": lon,
        "radius": radius,
        "limit": limit,
        "type": type_
    }
    r = requests.get(BASE_URL+"articles", params=payload)
    articles = r.json()['articles']

    return articles

exif = get_exif_data('IMG2.JPG')
lat, lon = gps_coord(exif)

articles = articles(lat, lon, 1000, 10, '')[0]
for article in articles:
    if 'title' in article:
        print article[0]

