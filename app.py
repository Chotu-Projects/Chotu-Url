from os import getenv

from dotenv import load_dotenv
from flask import Flask, render_template, request
from flask import redirect, send_from_directory
from rich.console import Console

import Database.database as dbs
from Encoder.generator import base58, encrypt
from utils.config import load_config

# config
config = load_config()

# setup Python-Rich
console = Console()

# Database connect and setup
load_dotenv()

mongo_uri = getenv("MONGO_URI")
database = getenv("DATABASE")
collection_name = getenv("COLLECTION")
hash_salt = getenv("SALT")

collection = dbs.connect(mongo_uri, database, collection_name)
dbs.setup(collection)

app = Flask(__name__)


@app.route('/', defaults={'chotu': ''})
@app.route('/<chotu>')
def home(chotu):
    if chotu:
        url = dbs.lookup(collection, chotu, hash_salt)
        if url:
            return redirect(url, code=302)
        else:
            return render_template('not_found.html'), 404
    return render_template('home.html')


@app.route('/chotu', methods=["POST"])
def chotu():
    found = False
    original_url = request.form.get('url')
    while not found:
        chotu_url_str, chotu_hash = base58(hash_salt)
        # encrypting the original url
        encrypted_url = encrypt(chotu_url_str, hash_salt, original_url)
        found = dbs.store(collection, chotu_hash, encrypted_url)

    chotu_url = config['domain'] + chotu_url_str

    data = {
        'url': original_url,
        'chotu_url': chotu_url,
        'counter_url': f"{config['completeDomain']}count?url={chotu_url_str}",
        'social': {
            'facebook': f'https://www.facebook.com/sharer/sharer.php?u={chotu_url}',
            'twitter': f'https://twitter.com/share?url={chotu_url}',
            'pinterest': f'https://pinterest.com/pin/create/link/?url={chotu_url}',
            'tumblr': f'https://www.tumblr.com/share/link?url={chotu_url}',
            'whatsapp': f'whatsapp://send?text={chotu_url}'
        }
    }

    return render_template('chotu.html', data=data)


@app.route('/counter')
def counter():
    data = {
        "host": config['completeDomain']
    }
    return render_template('counter.html', data=data)


@app.route('/count', methods=['GET'])
def count():
    chotu_url = request.args['url']

    print(chotu_url)
    if (config['domain'] in chotu_url) \
            or ('http://' + config['domain']) in chotu_url \
            or ('https://' + config['domain']) in chotu_url:

        chotu_url = chotu_url.split(config['domain'][-5:])[1]

    views = dbs.fetch_views(collection, chotu_url, hash_salt)

    return render_template('count.html', views=views)


@app.route('/underdev')
def underdev():
    return render_template('underdev.html')


# Error Handling
@app.errorhandler(404)
def not_found(_):
    return render_template('not_found.html'), 404


# Robots.txt and Sitemap
@app.route('/sitemap.xml')
@app.route('/robots.txt')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        app.static_folder, 'favicon.ico',
        mimetype='image/vnd.microsoft.icon')


if __name__ == "__main__":
    app.run(debug=True)
