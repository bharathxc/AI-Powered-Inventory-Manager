import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_books():
    base_url = 'http://books.toscrape.com/catalogue/page-{}.html'
    all_books = []

    for page in range(1, 6):  # Scrape 5 pages (20 books each)
        response = requests.get(base_url.format(page))
        soup = BeautifulSoup(response.text, 'lxml')
        books = soup.select('article.product_pod')

        for book in books:
            title = book.h3.a['title']
            price = float(book.select_one('p.price_color').text[2:])
            rating = book.p['class'][1]  # Ex: 'One', 'Two', etc.
            all_books.append({
                'title': title,
                'price': price,
                'rating': rating
            })

    df = pd.DataFrame(all_books)
    df.to_csv('data/raw_data.csv', index=False)
    print("Saved data/raw_data.csv")

if __name__ == '__main__':
    scrape_books()
