"""
Файл для імпорту JSON файлів authors.json та quotes.json у MongoDB. Використовує pymongo для
підключення до бази даних та виконання операцій вставки/оновлення. Перед запуском переконайтеся,
що у вас є файл config.ini з правильними параметрами підключення до MongoDB. Обробка помилок
включає в себе вивід повідомлень про успішну обробку та помилки під час імпорту. У разі
повторного запуску скрипта, існуючі записи будуть оновлені, а нові додані завдяки використанню
upsert=True. Якщо файли authors.json або quotes.json відсутні, скрипт виведе повідомлення про це.
"""
import os
import configparser
import json
from pymongo import MongoClient

# 1. Читаємо конфіг
config = configparser.ConfigParser()
config.read("config.ini")

USER = config["DB"]["USER"]
PASS = config["DB"]["PASS"]
DB_NAME = config["DB"]["DB_NAME"]
DOMAIN = config["DB"]["DOMAIN"]

uri = f"mongodb+srv://{USER}:{PASS}@{DOMAIN}/{DB_NAME}?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client[DB_NAME]

authors_collection = db["authors"]
quotes_collection = db["quotes"]

def import_json():
    """ Функція імпорту JSON файлів authors.json та quotes.json у MongoDB. """
    try:
        if os.path.exists("authors.json"):
            with open("authors.json", "r", encoding="utf-8") as f:
                authors = json.load(f)
            for author in authors:
                authors_collection.update_one(
                    {"fullname": author["fullname"]},
                    {"$set": author},
                    upsert=True
                )
            print(f"✅ Processed {len(authors)} authors")
        else:
            print("⚠️ authors.json not found")

        if os.path.exists("quotes.json"):
            with open("quotes.json", "r", encoding="utf-8") as f:
                quotes = json.load(f)
            for quote in quotes:
                quotes_collection.update_one(
                    {"quote": quote["quote"]},
                    {"$set": quote},
                    upsert=True
                )
            print(f"✅ Processed {len(quotes)} quotes")
        else:
            print("⚠️ quotes.json not found")

    except Exception as e:
        print(f"❌ Error importing JSON: {e}")
        
if __name__ == "__main__":
    import_json()
