import requests
from bs4 import BeautifulSoup
import lxml
import pandas as pd
import re

names = []
ages = []
genders = []
breeds = []
descriptions = []
urls = []
images = []
current_weights = []
sizes = []
adoption_urls = []


site = requests.get('https://ny-petrescue.org/Adopt-Dogs')
source_code = site.content
soup = BeautifulSoup(source_code, 'lxml')
dog_cards = soup.find_all('div', class_='blogEventsThreeColItem')

print(f'Total dog profiles found: {len(dog_cards)}, start scraping details...')

image_div = soup.find_all("div", class_="bcImage adoption")

for i in image_div:
    style = i.get("style", "")
    match = re.search(r"url\(['\"]?(.*?)['\"]?\)", style)
    if match:
        relative_path = match.group(1)
        full_url = f"https://ny-petrescue.org{relative_path}"
        images.append(full_url)
    else:
        print("No image URL found")

for card in dog_cards:
    link = f"https://ny-petrescue.org/{card.a['href']}"
    urls.append(link)

for url in urls:
    dog_site = requests.get(url)
    dog_source = dog_site.content
    dog_soup = BeautifulSoup(dog_source, 'lxml')
    name = dog_soup.find('h3').text.strip()
    names.append(name)
    info_items = dog_soup.find('ul', class_='details').find_all('li')
    age = info_items[1].text.strip().replace('Age: ', '')
    ages.append(age)
    gender = info_items[3].text.strip().replace ('Gender: ', '')
    genders.append(gender)
    breed = info_items[2].text.strip().replace('Breed: ', '')
    breeds.append(breed)
    current_weight = info_items[5].text.strip().replace('Weight: ', '').replace(' lbs.', '')
    current_weights.append(current_weight)
    size = info_items[4].text.strip()
    sizes.append(size)

    description_element = dog_soup.find('div', class_='mainContentArea').text.strip()
    start_marker = "A little About"
    end_marker = "Back"
    start_id = description_element.find(start_marker)
    end_id = description_element.find(end_marker, start_id)
    if start_id != -1 and end_id != -1:
        description = description_element[start_id:end_id].strip()
        descriptions.append(description)
    else:
        print("Markers not found in the description.")
    adoption_url = 'https://www.cognitoforms.com/PetRescue2/PetRescueDogApplication'
    adoption_urls.append(adoption_url)
    
if len(names)==len(ages)==len(genders)==len(breeds)==len(descriptions)==len(images)==len(adoption_urls):
    df = pd.DataFrame({
        'Name': names,
        'Age': ages,
        'Gender': genders,
        'Breed': breeds,
        'Description': descriptions,
        'Image_URL': images,
        'Adoption_URL': adoption_urls,
        'current_weights': current_weights,
        'sizes': sizes,
        'urls': urls
    })
    df.to_csv('/Users/galaxyrailwaytoto/Desktop/final_project/normalization/pet_rescue.csv', index=False)
    print('CSV file created successfully.')
else:
    print("Data length mismatch! Please check the data collected.")





