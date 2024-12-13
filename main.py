
import requests
from bs4 import BeautifulSoup
import pandas as pd

books = []
base_url = "https://books.toscrape.com/catalogue/page-{}.html"

response = requests.get(base_url.format(1))
response = response.content
soup = BeautifulSoup(response, 'html.parser')

pagination = soup.find('ul', class_='pager')
if pagination:
    total_pages = int(pagination.find('li', class_='current').text.strip().split()[-1])
    print(f"Total pages to scrape: {total_pages}")
else:
    total_pages = 1  
    print("Pagination not found, assuming only one page.")

for i in range(1, total_pages + 1):
    print(f"Scraping page {i}...")
    url = base_url.format(i)
    response = requests.get(url)
    response = response.content
    soup = BeautifulSoup(response, 'html.parser')
    ol = soup.find('ol')
    articles = ol.find_all('article', class_='product_pod')
    for article in articles:
        image = article.find('img')
        title = image.attrs['alt']
        starTag = article.find('p')
        star = starTag['class'][1]
        price = article.find('p', class_='price_color').text
        price = float(price[1:])
        books.append([title, star, price])

df = pd.DataFrame(books, columns=['Title', 'Star Rating', 'Price'])
df.to_csv('books1.csv', index=False)
print("Data saved to books.csv")
