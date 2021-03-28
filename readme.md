# Extracting informations from web site "Books to Scrape" :

## Description
Creating a python script that collect information from the web site "Books to scrape", From "Books to scrape" website url, main.py will extract all URLs books for a each category and extract the following informationgs if founded :
-product_page_url
-universal_ product_code (upc)
-title
-price_including_tax
-price_excluding_tax
-number_available
-product_description
-category
-review_rating
-image_url

Then transform all informations needed and load them in csv files.

## Installation:
This project was created with Python 3.9
Requirements subsection needed :
- beautifulsoup4==4.9.3
- bs4==0.0.1
- certifi==2020.12.5
- chardet==4.0.0
- idna==2.10
- lxml==4.6.2
- requests==2.25.1
- soupsieve==2.2
- urllib3==1.26.3

## Setup for Windows :
After downloading the project from Github, extract it to a location of your choice or clone it if uou are using git.

Then, using cmd, go to the location of the project, create a virtual environment and install packages from requirements.txt as follow :

$ CD ../path/to/the/project
$ py -m venv env
$ execute activate.bat located in env\Scripts
$ py -m pip install -U pip
$ pip install -r requirements.txt
$ then execute main.py

