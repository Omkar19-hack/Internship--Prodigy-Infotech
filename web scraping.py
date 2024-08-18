import requests
from bs4 import BeautifulSoup
import csv

# URL of the website to scrape
url = "http://books.toscrape.com/catalogue/page-1.html"

# Open CSV file to save data
with open('books.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Title', 'Price', 'Rating']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Loop through all the pages
    while True:
        # Send a GET request to the URL
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all the book elements
        books = soup.find_all('article', class_='product_pod')

        # Extract details for each book
        for book in books:
            title = book.h3.a['title']
            price = book.find('p', class_='price_color').text
            rating = book.p['class'][1]  # Rating is stored as a class (e.g., 'star-rating Three')

            # Write data to CSV
            writer.writerow({'Title': title, 'Price': price, 'Rating': rating})


        next_button = soup.find('li', class_='next')
        if next_button:
            next_url = next_button.a['href']
            url = "http://books.toscrape.com/catalogue/" + next_url
        else:
            break

print("Scraping completed. Data saved to books.csv")
