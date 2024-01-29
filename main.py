import requests
from bs4 import BeautifulSoup
import json

def get_quotes(url):
    quotes = []
    authors = {}
    while url:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        for quote in soup.find_all("div", class_="quote"):
            text = quote.find("span", class_="text").get_text()
            author = quote.find("small", class_="author").get_text()
            tags = [tag.get_text() for tag in quote.find_all("a", class_="tag")]

            quotes.append({"text": text, "author": author, "tags": tags})
            
            if author not in authors:
                author_page_link = quote.find_next("a")["href"]
                authors[author] = get_author_info("http://quotes.toscrape.com" + author_page_link)

        next_btn = soup.find("li", class_="next")
        url = "http://quotes.toscrape.com" + next_btn.find("a")["href"] if next_btn else None

    return quotes, authors

def get_author_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    born_date = soup.find("span", class_="author-born-date").get_text()
    born_location = soup.find("span", class_="author-born-location").get_text()
    description = soup.find("div", class_="author-description").get_text()
    return {"born_date": born_date, "born_location": born_location, "description": description}

quotes, authors = get_quotes("http://quotes.toscrape.com")

with open(r'json/quotes.json', 'w') as f:
    json.dump(quotes, f, indent=4)

with open(r'json/authors.json', 'w') as f:
    json.dump(authors, f, indent=4)
