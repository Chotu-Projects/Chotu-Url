from datetime import datetime

from pymongo import MongoClient
from rich.console import Console

from Encoder.generator import decrypt, hash_chotu

# setup Python-Rich
console = Console()


def connect(mongo_uri, database, collection_name):
    """
    Connect to mongodb database and return collection
    """

    with console.status("[bright_magenta]Connecting to Database...") as _:
        try:
            client = MongoClient(mongo_uri)
            console.log("[bright_green]Fetched Client[/bright_green]✅")
        except Exception as error:
            console.log(
                "[bright_red]Error occured while fetching Client[/bright_red]❌")
            console.log(f"Error: {error}")

        try:
            dbs = client[database]
            console.log("[bright_green]Fetched DataBase[/bright_green]✅")
        except Exception as error:
            console.log(
                "[bright_red]Error occured while fetching Database[/bright_red]❌")
            console.log(f"Error: {error}")

        try:
            collection = dbs[collection_name]
            console.log("[bright_green]Fetched Collection[/bright_green]✅")
        except Exception as error:
            console.log(
                "[bright_red]Error occured while fetching Collection[/bright_red]❌")
            console.log(f"Error: {error}")

    return collection


def setup(collection, expire_days=60, inactive_days=15) -> None:
    """
    Create Index to automatically drop documents
    """

    expire_seconds = expire_days * 24 * 60 * 60
    inactive_seconds = inactive_days * 24 * 60 * 60

    try:
        collection.create_index("createdAt", expireAfterSeconds=expire_seconds)
        console.log(
            "[bright_green]Successfully created createdAt index[/bright_green]✅")
    except Exception as error:
        console.log(
            "[bright_red]Error occured while creating createdAt index[/bright_red]❌")
        console.log(f"Error: {error}")

    try:
        collection.create_index(
            'lastView', expireAfterSeconds=inactive_seconds)
        console.log(
            "[bright_green]Successfully created lastView index[/bright_green]✅")
    except Exception as error:
        console.log(
            "[bright_red]Error occured while creating lastView index[/bright_red]❌")
        console.log(f"Error: {error}")


def exists(collection, chotu_hash: str) -> bool:
    """
    Checks for availability of chotu_hash in database
    """
    data = collection.find_one({"_id": chotu_hash})
    if data:
        return True
    return False


def store(collection, chotu_hash:str, encrypted_url: str) -> bool:
    """
    Create and store new document/entry for chotu_url
    """

    # check for availability
    if exists(collection, chotu_hash):
        return False

    document = {
        "_id": chotu_hash,
        "chotuUrl": chotu_hash,
        "originalUrl": encrypted_url,
        "views": 0,
        "createdAt": datetime.utcnow(),
        "lastView": datetime.utcnow()
    }

    collection.insert_one(document)
    return True


def update_view(collection, chotu_hash, value=1, extend_date=datetime.utcnow()) -> bool:
    """
    Update the view of url and extends the expire-inactive
    """
    # update the view
    try:
        collection.update_one(
            {"_id": chotu_hash}, {
                # increment views
                "$inc": {"views": value},
                "$set": {"lastView": extend_date}
            }
        )
        console.log(
            "[bright_green]Successfully updated view and expireInactiveAt " \
                f"for `{chotu_hash}`[/bright_green]✅")
    except Exception as error:
        console.log(
            "[bright_red]Error occured while updating view or expireInactiveAt " \
                f"for `{chotu_hash}`[/bright_red]❌")
        console.log(f"Error: {error}")

    return True


def lookup(collection:str, chotu_url:str, salt:str) -> str:
    """
    Return original url associated with chotu url
    update view and extend inactive date
    """

    # hash the chotu_url
    chotu_hash = hash_chotu(chotu_url, salt)

    try:
        document = collection.find_one({'_id': chotu_hash})
        encrypted_url = document['originalUrl']

        original_url = decrypt(chotu_url, salt, encrypted_url)
        update_view(collection, chotu_hash)

        console.log(f"[bright_green]Successfully fetched {original_url} " \
            "[/bright_green]✅")
        return original_url
    except Exception as error:
        console.log(
            f"[bright_red]Error occured while fetching for {chotu_url} " \
                "[/bright_red]❌")
        console.log(f"Error: {error}")
        return ''
