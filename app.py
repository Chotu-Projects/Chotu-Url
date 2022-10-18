from os import getenv

from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect
from rich.console import Console

import Database.database as dbs
from Encoder.generator import base58, encrypt
from utils.config import load_config

PYTHONHASHSEED = 0

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
        'social': {
            'facebook': f'https://www.facebook.com/sharer/sharer.php?u={chotu_url}',
            'twitter': f'https://twitter.com/share?url={chotu_url}',
            'pinterest': f'https://pinterest.com/pin/create/link/?url={chotu_url}',
            'tumblr': f'https://www.tumblr.com/share/link?url={chotu_url}',
            'whatsapp': f'whatsapp://send?text={chotu_url}'
        }
    }

    return render_template('chotu.html', data=data)


@app.route('/test_chotu')
def test_chotu():
    return render_template('chotu.html')


# Error Handling
@app.errorhandler(404)
def not_found(_):
    return render_template('not_found.html'), 404


if __name__ == "__main__":
    app.run(debug=True)
