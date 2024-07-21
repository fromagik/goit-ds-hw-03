import requests
from bs4 import BeautifulSoup
import json

quotes_list = []
authors_list = []
visited_authors = set() # Сет для перевірки індивідуальності автора

url = 'https://quotes.toscrape.com/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')

# Знайдемо всі елементи з класом 'page'
page_elements = soup.find_all('li', class_='page')
if page_elements:
    last_page = max([int(page_element.text) for page_element in page_elements])
else:
    last_page = 1

#Проходимо по всіх сторінках
for page in range(1, last_page + 1):
    url = f'https://quotes.toscrape.com/page/{page}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    quotes_div = soup.find_all('div', class_="quote")

    # Ітерація по всім квотам і з кожної витягуємо потрібну інформацію
    for quote_div in quotes_div:
        quote = quote_div.find('span', class_='text').get_text()
        author = quote_div.find('small', class_='author').get_text()
        tags = [tag.get_text() for tag in quote_div.find_all('a', class_='tag')]

        # Додаємо всю інформацію до списку квот
        quotes_list.append({
            'quote' : quote,
            'author' : author,
            'tags' : tags
        })  

        if author not in visited_authors: # Якщо автор ще не в сеті “індивідуальності“ 
            visited_authors.add(author) # Додаємо його туди
            author_page = quote_div.find('a')['href'] # і витагуємо url для кожного автора 
            url = f'https://quotes.toscrape.com/{author_page}'
            response = requests.get(url)
            author_soup = BeautifulSoup(response.text, 'lxml')
            author_name = author_soup.find('h3', class_='author-title').get_text()
            author_born = author_soup.find('span', class_='author-born-date').get_text()
            author_born_location = author_soup.find('span', class_='author-born-location').get_text()
            author_description = author_soup.find('div', class_="author-description").get_text()
            
            #Додаємо інформацію про автора в список 
            authors_list.append({
                "fullname" : author_name,
                "born_date" : author_born,
                "born_location" : author_born_location,
                "description" : author_description
            })

# Записуємо всю інформацію в файлі json
with open('quotes.json', 'w', encoding='utf-8') as f:
    json.dump(quotes_list, f, ensure_ascii=False, indent=4)

with open('authors.json', 'w', encoding='utf-8') as f:
    json.dump(authors_list, f, ensure_ascii=False, indent=4)


    


