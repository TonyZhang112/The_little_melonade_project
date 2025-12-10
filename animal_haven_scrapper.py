import requests
from bs4 import BeautifulSoup
import lxml
import pandas as pd

names = []
ages = []
genders = []
breeds = []
descriptions = []
urls = []
images = []
adoption_urls = []
current_weights = []


site = requests.get('https://animalhaven.org/adopt/dogs?sort=age')
source_code = site.content
soup = BeautifulSoup(source_code, 'lxml')
dog_cards = soup.find_all('article', class_='pet-preview')
for card in dog_cards:
    link = f"https://animalhaven.org{card.a['href']}"
    urls.append(link)

print(f'Total dog profiles found: {len(urls)}, start scraping details...')

for url in urls: 
    dog_site = requests.get(url)
    dog_source = dog_site.content
    dog_soup = BeautifulSoup(dog_source, 'lxml')
    name = dog_soup.find('h1', class_= 'pet-profile__name').text.strip()
    names.append(name)
    info_items = dog_soup.find('ul', class_='pet-profile__subtitle').find_all('li')
    breed = info_items [1].text.strip()
    breeds.append(breed)
    age_text = info_items[2].text.strip()
# 1. Clean up labels and non-standard characters
    age_temp = age_text.replace('\n', ' ').replace('\xa0', ' ').replace('•', '').replace('Age:', '').strip()
# 2. Normalize whitespace by splitting on any whitespace and rejoining with a single space
    age = " ".join(age_temp.split()) 
    ages.append(age)
    gender = info_items [0].text.strip().replace('.','')
    genders.append(gender)
    description = dog_soup.find('div', class_='pet-profile__description-text').text.strip()
    descriptions.append(description)
    image = dog_soup.find('div', class_='pet-gallery__active-image').find('img')['src']
    images.append(image)
    adoption_url_element = dog_soup.select_one('a.button--purple[href*="adoption-interest"]').get('href')
    adoption_url = f"https://animalhaven.org{adoption_url_element}"
    adoption_urls.append(adoption_url)
    weight = dog_soup.find('dd', class_='pet-profile__property-description').text.strip().replace(' lbs', '')
    current_weights.append(weight)
    

print('data collection complete, saving to CSV...')

df = pd.DataFrame({
    'Name': names,
    'Age': ages,
    'Gender': genders,
    'Breed': breeds,
    'Description': descriptions,
    'Image_URL': images,
    'Adoption_URL': adoption_urls,
    'current_weights': current_weights,
    'urls': urls
})
df.to_csv('/Users/galaxyrailwaytoto/Desktop/final_project/normalization/animal_heaven_dogs.csv', index=False)

print('CSV file created successfully.')
    




