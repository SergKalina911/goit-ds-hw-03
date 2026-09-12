""" 
Файл scraper.py містить функцію scrape_quotes(), яка виконує скрапінг цитат та авторів з сайту
quotes.toscrape.com. Використовує бібліотеки requests та BeautifulSoup для отримання та парсингу
HTML сторінок. Збирає цитати, авторів та теги, а також деталі про авторів (повне ім'я, дата
народження, місце народження, опис). Результати зберігаються у файли quotes.json та authors.json
у форматі JSON. Перериває работу у разі відсутності наступної сторінки або помилки запиту. Перед
запуском переконайтеся, що у вас встановлені бібліотеки requests та BeautifulSoup.
"""
import requests
from bs4 import BeautifulSoup
import json

BASE_URL = "http://quotes.toscrape.com"

def scrape_quotes():
    """
    Функція для скрапінгу цитат та авторів з сайту quotes.toscrape.com. Повторює запити до
    сторінок, поки не буде досягнуто кінця пагінації. Повертає список цитат та словник авторів,
    які зберігаються у файли quotes.json та authors.json.  
    """
    quotes = []
    authors = {}
    page = 1

    while True:
        url = f"{BASE_URL}/page/{page}/"
        response = requests.get(url)
        if response.status_code != 200:
            break

        soup = BeautifulSoup(response.text, "html.parser")
        quote_blocks = soup.select(".quote")

        if not quote_blocks:
            break

        for q in quote_blocks:
            text = q.select_one(".text").get_text(strip=True)
            author = q.select_one(".author").get_text(strip=True)
            tags = [t.get_text(strip=True) for t in q.select(".tags .tag")]

            quotes.append({"tags": tags, "author": author, "quote": text})

            # збираємо дані про автора
            author_link = BASE_URL + q.select_one("a")["href"]
            if author not in authors:
                author_page = requests.get(author_link)
                soup_author = BeautifulSoup(author_page.text, "html.parser")
                fullname = soup_author.select_one(".author-title").get_text(strip=True)
                born_date = soup_author.select_one(".author-born-date").get_text(strip=True)
                born_location = soup_author.select_one(".author-born-location").get_text(strip=True)
                description = soup_author.select_one(".author-description").get_text(strip=True)

                authors[author] = {
                    "fullname": fullname,
                    "born_date": born_date,
                    "born_location": born_location,
                    "description": description
                }

        page += 1

    # зберігаємо у файли
    with open("quotes.json", "w", encoding="utf-8") as f:
        json.dump(quotes, f, ensure_ascii=False, indent=4)

    with open("authors.json", "w", encoding="utf-8") as f:
        json.dump(list(authors.values()), f, ensure_ascii=False, indent=4)

    print("✅ Scraping complete. Files saved: quotes.json, authors.json")

if __name__ == "__main__":
    scrape_quotes()
