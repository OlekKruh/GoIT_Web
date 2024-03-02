import json
import requests
from bs4 import BeautifulSoup

url = 'https://quotes.toscrape.com'
dict_of_quotes = []
dict_of_authors_bio = []
counter = 1

headers = {
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
}
while url:
    my_requests = requests.get(url, headers=headers)
    print('my_requests')
    src = my_requests.text
    soup = BeautifulSoup(src, 'lxml')

    quotes = soup.find_all(class_='quote')
    for quote in quotes:
        print(f'Quote: {counter}')
        counter += 1
        text = quote.find('span').text
        author = quote.find('small').text
        tags = [tag.text for tag in quote.find_all(class_='tag')]
        dict_of_quotes.append(
            {
                'Author': author,
                'Quote': text,
                'Tags': tags,
            }
        )

        author_bio_link = 'https://quotes.toscrape.com' + quote.find('a')['href']
        my_author_bio_requests = requests.get(author_bio_link, headers=headers)
        print(f'my_author_bio_requests\n{author_bio_link}')
        src_author = my_author_bio_requests.text
        author_soup = BeautifulSoup(src_author, 'lxml')

        fullname = author_soup.find(class_='author-title').text
        born_date = author_soup.find(class_='author-born-date').text
        born_location = author_soup.find(class_='author-born-location').text
        description = author_soup.find(class_='author-description').text.strip()
        dict_of_authors_bio.append(
            {
                'Fullname': fullname,
                'Born_Date': born_date,
                'Born_Location': born_location,
                'Description': description,
            }
        )

    # Navigation to next page
    next_page_href = soup.find(class_='next')
    if next_page_href:
        next_page_link = 'https://quotes.toscrape.com' + next_page_href.find('a')['href']
        url = next_page_link
        print(f'Navigation to page: {url}')
    else:
        print('Link to next page not found.')
        break

with open(f'authors_quotes.json', 'a', encoding='utf-8') as file:
    json.dump(dict_of_quotes, file, indent=4, ensure_ascii=False)

with open(f'authors_bio.json', 'a', encoding='utf-8') as file:
    json.dump(dict_of_authors_bio, file, indent=4, ensure_ascii=False)
