from pymongo import MongoClient, errors
import json

def get_connection(): # Функція для підключення до БД
    try:
        client = MongoClient('mongodb://localhost:27017/')
        return client.parse_database
    except errors.ConnectionError as e:
        print(f"Connection error: {e}")
        return None
    
def inser_quotes():
    # Функція для добавлення квотів 
    db = get_connection()
    if db is None:
        return
    collection = db.quotes

    # Відкриваємо файл json для читання 
    with open('quotes.json', 'r', encoding='utf-8') as f:
        quotes = json.load(f)
     
    try:
        for quote in quotes:
            # Додаємо всю інформацію в БД звертаючсь до ключа в файлі json
            collection.insert_one({
                "quote": quote['quote'],
                "author": quote["author"],
                "tags": quote["tags"]
            })
            print("Document inserted successfully")
    except errors.PyMongoError as e:
        print(f"Error inserting document: {e}")

# функція для додавання авторів працює так само як попередня 
def inser_authors():
    db = get_connection()
    if db is None:
        return
    collection = db.authors

    with open('authors.json', 'r', encoding='utf-8') as f:
        authors = json.load(f)
     
    try:
        for author in authors:
            collection.insert_one({
                "fullname": author["fullname"],
                "born_date": author["born_date"],
                "born_location": author["born_location"],
                "description" : author["description"]
            })
            print("Document inserted successfully")
    except errors.PyMongoError as e:
        print(f"Error inserting document: {e}")
