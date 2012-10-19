from flask import Blueprint, render_template, request

main = Blueprint('main', __name__)
from petascope_cache import db
from petascope_cache.models import Cached_WCPS
from petascope_cache import mime_types
from petascope_cache import app
from petascope_cache.settings import PETASCOPE_BASE, IMAGE_CACHE
from flask import send_file


def index():
    return render_template('index.html')

def cached_request():
    #app.logger.debug('some thing i wrote in the log')

    import hashlib
    import re
    m = hashlib.md5()
    get_args = request.args
    #app.logger.debug('blah %s' % get_args['query'])
    if 'query' not in  get_args:
        app.logger.debug('query is none')
        return 'Bad Request : no query parameter found', 400
    flattened_query = "".join(get_args['query'].split())
    print flattened_query
    m.update(flattened_query)
    encoding = re.findall(r'"(png|jpeg|csv|netcdf|tiff)"', flattened_query)
    if encoding:
        found_mime = str(encoding[0])
    else:
        encoding = re.findall(r'"(.+[a-zA-Z])"', flattened_query)
        error = 'Encoding requested is not supported: "%s"' % encoding[0]
        return render_template('wcps_error.html', query=get_args['query'] , error=error, encodings=mime_types), 500
    #found_mime = str(re.findall(r'"(png|jpeg|csv|netcdf|tiff)"',flattened_query)[0])
    print found_mime
    wcps_hash = m.hexdigest()
    cached = Cached_WCPS.query.filter_by(hash=wcps_hash).first()
    if cached:
        from datetime import datetime
        print "##### sending cached file : %s" % cached
        t_dif = datetime.utcnow() - cached.date_added
        print (t_dif.seconds / 60) % 60
        #if (t_dif.seconds / 60) % 60 > app.config['CACHE_TIME_TO_KEEP']:
        #    print "cache file is TOO OLD. caching again"
        #    return cache_and_send(get_args, wcps_hash, found_mime, cached_wcps=cached)
        return send_file(cached.result, cached.mime)
    else:
        return cache_and_send(get_args, wcps_hash, found_mime)

def cache_and_send(get_args, wcps_hash, found_mime, cached_wcps=None):
        print "##### new query detected - caching query"
        if cached_wcps:
            delete_cache_entry(cached_wcps)
        data = fetch_wcps_response(query=get_args['query'])
        #check_response(mime_types[found_mime][0], data)
        if 'xml' in check_response(mime_types[found_mime][0], data):
            from pygments import highlight
            from pygments.lexers import XmlLexer
            from pygments.formatters import HtmlFormatter
            hylited = highlight(data.read(), XmlLexer(), HtmlFormatter())
            app.logger.debug(hylited)
            return render_template('wcps_test.html', wcps=hylited, query=get_args['query']), 500
        newfile = save_wcps_response(data, wcps_hash, mime_types[found_mime][1])
        new_cache = Cached_WCPS(wcps_hash, newfile, mime_types[found_mime][0])
        print "##### save query %s" % new_cache
        db.session.add(new_cache)
        db.session.commit()
        return send_file(newfile, mime_types[found_mime][0])

def delete_cache_entry(key):
    print "deleting %s as it is too old" % key
    db.session.delete(key)
    db.session.commit()
    

def check_response(expected_mime, data):
    if data.info()['Content-Type'] != expected_mime:
        app.logger.error(data.info()['Content-Type'])
        if 'xml' in data.info()['Content-Type']:
            return 'text/xml'
        if expected_mime == 'text/csv' and data.info()['Content-Type'] == 'text/plain; charset=UTF-8':
            return 'text/csv'
    else:
        return expected_mime
    


def fetch_wcps_response(query=None):
    if query:
        import urllib2
        import urllib
        data = {}
        #data['query'] = urllib.quote_plus(query)
        #url_values = urllib.urlencode(data)
        url = PETASCOPE_BASE
        full_url = url + '?query=' + urllib.quote(query.replace('+', '%2B'), safe='~(){}%')
        data = urllib2.urlopen(full_url)
        print data.info()
        return data
    return None

def save_wcps_response(data, hashed, mime):
    outfile = open('%s%s.%s' % (IMAGE_CACHE,hashed, mime), 'w')
    outfile.write(data.read())
    outfile.close()
    return '%s%s.%s' % (IMAGE_CACHE,hashed, mime)
    


