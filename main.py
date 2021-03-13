import requests
from bs4 import BeautifulSoup
import urllib.parse
import csv

product_page_url = "http://books.toscrape.com/catalogue/the-bear-and-the-piano_967/index.html"

response = requests.get(product_page_url)

html = response.content
soup = BeautifulSoup(html, 'html.parser')

universal_product_code = soup.find("td").text

print(product_page_url)
print(universal_product_code)

title = soup.find("h1").text

print(title)

price_including_tax = soup.find_all('td')[3].text

print(price_including_tax)

price_excluding_tax = soup.find_all('td')[2].text

print(price_excluding_tax)

number_available = soup.find_all('td')[5].text

print(number_available[10:12])

product_description = soup.find('div',{"id": 'product_description'}).find_next_sibling('p').text

print(product_description)

category = soup.find_all('li')[2].text

print(category)

review_rating = soup.find('p',{'class':'star-rating'})['class'][1]

print(review_rating)

link = soup.find('img',{'alt':"The Bear and the Piano"})['src']

home_url = 'http://books.toscrape.com'

image_url = urllib.parse.urljoin(home_url, link)


print(image_url)


with open('data.csv', 'w', newline='') as fp:
     a = csv.writer(fp)
     data=[['product_page_url','universal_product_code','title','price_including_tax','price_excluding_tax','number_available','product_description','category','review_rating','image_url'],
           [product_page_url,universal_product_code,title,price_including_tax,price_excluding_tax,number_available[10:12],product_description,category,review_rating,image_url]]
     a.writerows(data)