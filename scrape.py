# importing necessary modules

import urllib.request
from bs4 import BeautifulSoup
import csv

# a variable for the maximum amount of pages to scrape from (current amount of pages available is 110)
max_pages = 10


# the .csv-file is opened in write-mode. Headers are defined to the file (fieldnames)
with open('yritykset.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    fieldnames = ['Nimi', 'Verkkosivut', 'Osoite']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel')
    writer.writeheader()


    # definition of HTTP request headers. In this case only user agent is defined
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }


    # this for loop is used for iterating through the scrapable pages until the loop reaches the max_pages value
    for page_number in range(1, max_pages + 1):
        url = f"https://www.finder.fi/search?what=sovellukset+ja+ohjelmistot&type=company&page={page_number}"

        request = urllib.request.Request(url, headers=headers)
        html = urllib.request.urlopen(request).read()

        soup = BeautifulSoup(html, 'html.parser')



        #scraping the website data using beautifulsoup to parse the output
        for company in soup.find_all('div', class_='SearchResult--compact'):
            name_element = company.find('a', class_='SearchResult__ProfileLink')
            website_element = company.find('a', class_='undefined')
            address_element = company.find('a', class_='SearchResult__Link')

            if name_element:
                name = name_element.text.strip()
            else:
                name = "Nimeä ei löydy" # prints to the .csv if the company's name is unavailable

            if website_element:
                # fetching the website from title-attribute
                website = website_element.get('title', '').strip()
            else:
                website = "Verkkosivuja ei löydy" # prints if the company's website is unavailable

            if address_element:
                # 0fetching the address from the href-attribute
                address_url = address_element['href']

                # the address is split from the URL and parsed
                parsed_address = urllib.parse.urlparse(address_url)
                address_params = urllib.parse.parse_qs(parsed_address.query)
                address = address_params.get('address', [''])[0]
            else:
                address = "Osoitetta ei löydy" # prints if address is unavailable

            # scraped data is written to the .csv
            writer.writerow({'Nimi': name, 'Verkkosivut': website, 'Osoite': address})

        print(f"Tiedot kirjattu sivulta {page_number} yritykset.csv-tiedostoon.") # prints out the current scraped page
