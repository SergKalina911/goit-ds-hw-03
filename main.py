""" 
Файл main.py містить функції для роботи з базою даних MongoDB, що дозволяють створювати, читати,
оновлювати та видаляти документи у колекції "cats". Використовує бібліотеку pymongo для підключення
до бази даних та виконання CRUD-операцій. Конфігураційні параметри для підключення до бази даних
зчитуються з файлу config.ini. Функції включають:
- create_cat: створює нового кота
- read_all: читає всі документи
- read_by_name: читає документ за ім'ям
- update_age: оновлює вік кота
- add_feature: додає нову характеристику коту
- delete_by_name: видаляє кота за ім'ям
- delete_all: видаляє всі документи
Використання функцій демонструється у блоці if __name__ == "__main__":, де створюється новий кіт,
читаються всі документи, оновлюється вік та додається нова характеристика, після чого кіт
видаляється (для цього треба розкоментувати останній рядок).
"""

import configparser
from pymongo import MongoClient
from bson.objectid import ObjectId

# Читаємо конфіг
config = configparser.ConfigParser()
config.read("config.ini")

USER = config["DB"]["USER"]
PASS = config["DB"]["PASS"]
DB_NAME = config["DB"]["DB_NAME"]
DOMAIN = config["DB"]["DOMAIN"]

uri = f"mongodb+srv://{USER}:{PASS}@{DOMAIN}/{DB_NAME}?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client[DB_NAME]
cats = db["cats"]

# CREATE
def create_cat(name, age, features):
    try:
        result = cats.insert_one({"name": name, "age": age, "features": features})
        print(f"✅ Cat inserted with id {result.inserted_id}")
    except Exception as e:
        print(f"❌ Error inserting cat: {e}")

# READ
def read_all():
    for cat in cats.find():
        print(cat)

def read_by_name(name):
    cat = cats.find_one({"name": name})
    print(cat if cat else "❌ Cat not found")

# UPDATE
def update_age(name, new_age):
    result = cats.update_one({"name": name}, {"$set": {"age": new_age}})
    print(f"✅ Updated {result.modified_count} document(s)")

def add_feature(name, feature):
    result = cats.update_one({"name": name}, {"$push": {"features": feature}})
    print(f"✅ Updated {result.modified_count} document(s)")

# DELETE
def delete_by_name(name):
    result = cats.delete_one({"name": name})
    print(f"✅ Deleted {result.deleted_count} document(s)")

def delete_all():
    result = cats.delete_many({})
    print(f"✅ Deleted {result.deleted_count} document(s)")

if __name__ == "__main__":
    # приклад використання
    create_cat("barsik", 3, ["ходить в капці", "дає себе гладити", "рудий"])
    read_all()
    update_age("barsik", 4)
    add_feature("barsik", "любить рибу")
    read_by_name("barsik")
    
    # Розкоментуйте наступний рядок, щоб видалити кота "barsik" після перевірки
    # delete_by_name("barsik")
