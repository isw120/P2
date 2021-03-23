import requests
from bs4 import BeautifulSoup
import urllib.parse
import csv
import os


def extract(category_link, soup):
    li = soup.find_all("li", {'class': 'col-xs-6'})
    for elements in li:
        h3 = elements.find("h3")
        a = h3.find("a")
        href = a["href"]
        product_page_url = urllib.parse.urljoin(category_link, href)
        product_page_content = requests.get(product_page_url).content
        product_page_soup = BeautifulSoup(product_page_content, 'html.parser')

        universal_product_code = product_page_soup.find("td")
        title = product_page_soup.find("h1")
        price_including_tax = product_page_soup.find_all('td')[3]
        price_excluding_tax = product_page_soup.find_all('td')[2]
        number = product_page_soup.find_all('td')[5]
        product_description = product_page_soup.find('div', {"id": 'product_description'})
        category = product_page_soup.find_all('li')[2]
        review_rating = product_page_soup.find('p', {'class': 'star-rating'})['class'][1]
        link = product_page_soup.find('img')['src']

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

        file_name = image_url.split('/')[-1]
        r = requests.get(image_url, stream=True)
        with open("images/" + file_name, 'wb') as f:
            for chunk in r:
                f.write(chunk)

        data_list.append([product_page_url,
                        universal_product_code,
                        title, price_including_tax,
                        price_excluding_tax,
                        number_available,
                        product_description,
                        category,
                        review_rating,
                        image_url])


def check_for_next_page(category_link):

    category_page_content = requests.get(category_link).content
    category_soup = BeautifulSoup(category_page_content, 'html.parser')

    while True:
        pagination_button = category_soup.find('li', {"class": 'next'})
        if pagination_button is not None:
            extract(category_link, category_soup)
            hyperlink = pagination_button.find('a')
            url = hyperlink['href']
            next_page_url = urllib.parse.urljoin(category_link, url)
            category_page_content = requests.get(next_page_url).content
            category_soup = BeautifulSoup(category_page_content, 'html.parser')
        else:
            extract(category_link, category_soup)
            break


home_url = "http://books.toscrape.com"

response = requests.get(home_url)

web_page_content = response.content

soup = BeautifulSoup(web_page_content, 'html.parser')

ul = soup.find("ul", {'class': 'nav-list'}).find('ul')

al_lis = ul.find_all('li')

os.mkdir('images')
os.mkdir('categories')


for elem in al_lis:
    data_list = [['product_page_url',
                  'universal_product_code',
                  'title', 'price_including_tax',
                  'price_excluding_tax',
                  'number_available',
                  'product_description',
                  'category',
                  'review_rating',
                  'image_url']]
    li = elem.find('a')
    category_name = li.text
    href = li['href']
    category_link = urllib.parse.urljoin(home_url, href)
    check_for_next_page(category_link)
    with open('categories/' + category_name.rstrip().strip() + ".csv", 'w', newline='', encoding='utf-8') as fp:
        a = csv.writer(fp)
        a.writerows(data_list)
    del data_list[:]