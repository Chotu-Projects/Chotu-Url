from datetime import datetime

from dotenv import load_dotenv
from pymongo import MongoClient
from rich.console import Console

load_dotenv()
console = Console()

def connect(mongo_uri, database, collection_name):
    """
    Connect to mongodb database and return collection
    """

    with console.status("[bright_magenta]Connecting to DataBase...") as status:
        try:
            client = MongoClient(mongo_uri)
            console.log(f"[bright_green]Fetched Client[/bright_green]✅")
        except Exception as e:
            console.log(f"[bright_red]Error occured while fetching Client[/bright_red]❌")
            console.log(f"Error: {e}")
        
        try:
            db = client[database]
            console.log(f"[bright_green]Fetched DataBase[/bright_green]✅")
        except Exception as e:
            console.log(f"[bright_red]Error occured while fetching Database[/bright_red]❌")
            console.log(f"Error: {e}")
        
        try:
            collection = db[collection_name]
            console.log(f"[bright_green]Fetched Collection[/bright_green]✅")
        except Exception as e:
            console.log(f"[bright_red]Error occured while fetching Collection[/bright_red]❌")
            console.log(f"Error: {e}")

    return collection


def setup(collection, expire_days:int, inactive_days:int) -> None:
    """
    Create Index to automatically drop documents
    """

    expire_seconds = expire_days * 24 * 60 * 60
    inactive_seconds = inactive_days * 24 * 60 * 60

    try:
        collection.create_index("expireAt", expireAfterSeconds=expire_seconds)
        console.log(f"[bright_green]Successfully created expireAt index[/bright_green]✅")
    except Exception as e:
        console.log(f"[bright_red]Error occured while creating expireAt index[/bright_red]❌")
        console.log(f"Error: {e}")
    
    try:
        collection.create_index('expireInactiveAt', expireAfterSeconds=inactive_seconds)
        console.log(f"[bright_green]Successfully created expireInactiveAt index[/bright_green]✅")
    except Exception as e:
        console.log(f"[bright_red]Error occured while creating expireInactiveAt index[/bright_red]❌")
        console.log(f"Error: {e}")


def exists(collection, url_id:str) -> bool:
    data = collection.find_one({"_id": url_id})
    if data:
        return True
    else:
        return False


def store(collection, chotu_url:str, original_url:str) -> bool:
    
    if exists(collection, chotu_url):
        return False


    document = {
        "_id": chotu_url,
        "chotuUrl": chotu_url,
        "originalUrl": original_url,
        "views": 0,
        "createdAt": datetime.utcnow(),
        "expireAt": datetime.utcnow(),
        "expireFirst": datetime.utcnow()
    }

    collection.insert_one(document)
    return True


def update_view(collection, chotu_url, value=1, extend_date=):
    pass

# TEST
# collection = connect()
# status = store(collection, 'gogo', 'https://google.com')
# print(status)
