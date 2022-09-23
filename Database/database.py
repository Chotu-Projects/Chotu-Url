from datetime import datetime

from pymongo import MongoClient
from rich.console import Console

# setup Python-Rich
console = Console()


def connect(mongo_uri, database, collection_name):
    """
    Connect to mongodb database and return collection
    """

    with console.status("[bright_magenta]Connecting to DataBase...") as _:
        try:
            client = MongoClient(mongo_uri)
            console.log("[bright_green]Fetched Client[/bright_green]✅")
        except Exception as error:
            console.log(
                "[bright_red]Error occured while fetching Client[/bright_red]❌")
            console.log(f"Error: {error}")

        try:
            db = client[database]
            console.log("[bright_green]Fetched DataBase[/bright_green]✅")
        except Exception as error:
            console.log(
                "[bright_red]Error occured while fetching Database[/bright_red]❌")
            console.log(f"Error: {error}")

        try:
            collection = db[collection_name]
            console.log("[bright_green]Fetched Collection[/bright_green]✅")
        except Exception as error:
            console.log(
                "[bright_red]Error occured while fetching Collection[/bright_red]❌")
            console.log(f"Error: {error}")

    return collection


def setup(collection, expire_days: int, inactive_days: int) -> None:
    """
    Create Index to automatically drop documents
    """

    expire_seconds = expire_days * 24 * 60 * 60
    inactive_seconds = inactive_days * 24 * 60 * 60

    try:
        collection.create_index("expireAt", expireAfterSeconds=expire_seconds)
        console.log(
            "[bright_green]Successfully created expireAt index[/bright_green]✅")
    except Exception as error:
        console.log(
            "[bright_red]Error occured while creating expireAt index[/bright_red]❌")
        console.log(f"Error: {error}")

    try:
        collection.create_index(
            'expireInactiveAt', expireAfterSeconds=inactive_seconds)
        console.log(
            "[bright_green]Successfully created expireInactiveAt index[/bright_green]✅")
    except Exception as error:
        console.log(
            "[bright_red]Error occured while creating expireInactiveAt index[/bright_red]❌")
        console.log(f"Error: {error}")


def exists(collection, url_id: str) -> bool:
    """
    Checks for availability of url_id in database
    """
    data = collection.find_one({"_id": url_id})
    if data:
        return True
    return False


def store(collection, chotu_url: str, original_url: str) -> bool:
    """
    Create and store new document/entry for chotu_url
    """

    # check for availability
    if exists(collection, chotu_url):
        return False

    document = {
        "_id": chotu_url,
        "chotuUrl": chotu_url,
        "originalUrl": original_url,
        "views": 0,
        "createdAt": datetime.utcnow(),
        "expireAt": datetime.utcnow(),
        "expireInactiveAt": datetime.utcnow()
    }

    collection.insert_one(document)
    return True


def update_view(collection, chotu_url, value=1, extend_date=datetime.utcnow()):
    """
    Update the view of url and extends the expire-inactive
    """
    # check if url exists
    if exists(collection, chotu_url):
        # update the view
        try:
            collection.update_one(
                {"_id": chotu_url}, {
                    # increment views
                    "$inc": {"views": value},
                    "$set": {"expireInactiveAt": extend_date}
                }
            )
            console.log(
                f"[bright_green]Successfully updated view and expireInactiveAt \
                    for `{chotu_url}[/bright_green]✅")
        except Exception as error:
            console.log(
                f"[bright_red]Error occured while updating view or expireInactiveAt \
                    for `{chotu_url}`[/bright_red]❌")
            console.log(f"Error: {error}")

        return True
    return False
