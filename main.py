from pymongo import MongoClient, errors
import re

def get_connection(): # Функція для підключення до БД
    try:
        client = MongoClient('mongodb://localhost:27017/')
        return client.cats_database
    except errors.ConnectionError as e:
        print(f"Connection error: {e}")
        return None

def insert_one_doc(collection_name):
    # Функція для додавання одного файлу в БД, як параметр приймає назву колекції
    db = get_connection()
    if db is None:
        return
    collection = db[collection_name] 

    try: 
        name = str(input('Name: ')).strip()
        age = int(input('Age: '))
        features = input('Features (separated by spaces or punctuation): ').strip()
        features = re.split(r'[:.?;\s]+', features) # Розбивка всіх features на список за певними символами

        # Додавання інформації в коллекцію 
        collection.insert_one({
            "name": name,
            "age": age,
            "features": features
        })
        print("Document inserted successfully")
    except errors.PyMongoError as e:
        print(f"Error inserting document: {e}")
    except ValueError as e:
        print(f"Invalid input: {e}")

def read_all(collection_name): # Фукнція для виводу всієї інформації з БД, як параметр приймає назву колекції
    db = get_connection()
    if db is None:
        return []
    collection = db[collection_name]

    try:
        documents = collection.find({})
        return list(documents)
    except errors.PyMongoError as e:
        print(f"Error reading documents: {e}")
        return []

def read_doc_by_name(collection_name): # Функція для знаходження кота за ім‘ям, як параметр приймає назву колекції
    db = get_connection()
    if db is None:
        return []
    collection = db[collection_name]

    try:
        name = str(input('Name: '))
        documents = collection.find({'name': name})
        return list(documents)
    except errors.PyMongoError as e:
        print(f"Error reading document: {e}")
        return []

def update_age(collection_name): # Функція для зміни віку кота за його ім‘ям, як параметр приймає назву колекції
    db = get_connection()
    if db is None:
        return
    collection = db[collection_name]

    try:
        name = str(input('Name: '))
        new_value = int(input('New age: '))

        result = collection.update_one(
            {'name': name},
            {"$set": {'age': new_value}}
        )
        print(f"Updated documents: {result.modified_count}")
    except errors.PyMongoError as e:
        print(f"Error updating document: {e}")
    except ValueError as e:
        print(f"Invalid input: {e}")

def update_features(collection_name): # Функція для додавання нових features, як параметр приймає назву колекції
    db = get_connection()
    if db is None:
        return
    collection = db[collection_name]

    try:
        name = input('Name: ').strip()
        new_features = input('New features (separated by spaces or punctuation): ').strip()
        new_features = re.split(r'[\s,;:.]+', new_features)

        result = collection.update_one(
            {'name': name},
            {"$push": {'features': {"$each": new_features}}} # Додавання кожної feature окремо 
        )
        print(f"Updated documents: {result.modified_count}")
    except errors.PyMongoError as e:
        print(f"Error updating document: {e}")

def delete_cat(collection_name): # Функція для видалення кота за його ім‘ям, як параметр приймає назву колекції
    db = get_connection()
    if db is None:
        return
    collection = db[collection_name]

    try:
        name = str(input('Name of the cat to delete: ')).strip()
        result = collection.delete_one({'name': name})
        print(f"Documents deleted: {result.deleted_count}")
    except errors.PyMongoError as e:
        print(f"Error deleting document: {e}")

def delete_all(collection_name): # Функція для видалення всієї інформації в коллекції, як параметр приймає назву колекції
    db = get_connection()
    if db is None:
        return
    collection = db[collection_name]

    try:
        result = collection.delete_many({})
        print(f"Documents deleted: {result.deleted_count}")
    except errors.PyMongoError as e:
        print(f"Error deleting documents: {e}")

if __name__ == "__main__":
    # Приклади виклика функцій:
    # insert_one_doc('cat')
    # for doc in read_all('cat'):
    #     print(doc)
    # read_doc_by_name('cat')
    # update_age('cat')
    # update_features('cat')
    # delete_cat('cat')
    # delete_all('cat')
    pass
