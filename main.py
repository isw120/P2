import requests
from bs4 import BeautifulSoup
import urllib.parse
import csv

data_list = [['product_page_url',
              'universal_product_code',
              'title', 'price_including_tax',
              'price_excluding_tax',
              'number_available',
              'product_description',
              'category',
              'review_rating',
              'image_url']]

category_url = "http://books.toscrape.com/catalogue/category/books/fiction_10/index.html"

response = requests.get(category_url)

web_page_content = response.content

soup = BeautifulSoup(web_page_content, 'html.parser')


def extract():
    li = soup.find_all("li", {'class': 'col-xs-6'})
    for elements in li:
        h3 = elements.find("h3")
        a = h3.find("a")
        href = a["href"]
        product_page_url = urllib.parse.urljoin(category_url, href)
        response = requests.get(product_page_url)
        web_page_content = response.content
        soup2 = BeautifulSoup(web_page_content, 'html.parser')

        universal_product_code = soup2.find("td")
        title = soup2.find("h1")
        price_including_tax = soup2.find_all('td')[3]
        price_excluding_tax = soup2.find_all('td')[2]
        number = soup2.find_all('td')[5]
        product_description = soup2.find('div', {"id": 'product_description'})
        category = soup2.find_all('li')[2]
        review_rating = soup2.find('p', {'class': 'star-rating'})['class'][1]
        link = soup2.find('img')['src']

        if universal_product_code is None:
            universal_product_code = "empty"
        else:
            universal_product_code = universal_product_code.text
        if title is None:
            title = "empty"
        else:
            title = title.text
        if price_including_tax is None:
            price_including_tax = "empty"
        else:
            price_including_tax = price_including_tax.text
        if price_excluding_tax is None:
            price_excluding_tax = "empty"
        else:
            price_excluding_tax = price_excluding_tax.text
        if number is None:
            number_available = "empty"
        else:
            number = number.text
            number_available = number[10:12]
        if product_description is None:
            product_description = "empty"
        else:
            product_description = product_description.find_next_sibling('p').text
        if category is None:
            category = "empty"
        else:
            category = category.text
        if review_rating is None:
            review_rating = "empty"
        if link is None:
            image_url = "empty"
        else:
            home_url = 'http://books.toscrape.com'
            image_url = urllib.parse.urljoin(home_url, link)

        print(product_page_url)
        print(universal_product_code)
        print(title)
        print(price_including_tax)
        print(price_excluding_tax)
        print(number_available)
        print(product_description)
        print(category)
        print(review_rating)
        print(image_url)

        all_elements = [product_page_url,
                        universal_product_code,
                        title, price_including_tax,
                        price_excluding_tax,
                        number_available,
                        product_description,
                        category,
                        review_rating,
                        image_url]

        data_list.append(all_elements)


while True:
    pagination_button = soup.find('li', {"class": 'next'})
    if pagination_button is not None:
        extract()
        hyperlink = pagination_button.find('a')
        url = hyperlink['href']
        next_page_url = urllib.parse.urljoin(category_url, url)
        response = requests.get(next_page_url)
        html = response.content
        soup = BeautifulSoup(html, 'html.parser')
        extract()
    else:
        extract()
        break


with open('data.csv', 'w', newline='') as fp:
    a = csv.writer(fp)
    a.writerows(data_list)
