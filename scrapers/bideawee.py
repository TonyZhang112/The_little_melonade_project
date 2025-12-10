import requests
import pandas as pd
import re

API_KEY = "2a28d8ce-bc06-4573-bb6c-7c1828af54ee" 

names = []
ages = []
genders = []
breeds = []
descriptions = []
images = []
sizes = []
adoption_urls = []
urls = []

headers = {
    "x-api-key": API_KEY,
    "User-Agent": "Mozilla/5.0",
}

url = "https://www.shelterluv.com/api/v1/animals?status_type=publishable"
animal_list = requests.get(url, headers=headers).json()["animals"]

print(f'Total animal profiles found: {len(animal_list)}, start scraping details...')

for animal in animal_list:
    animal_id = animal["Internal-ID"]
    source_url = f"https://www.shelterluv.com/api/v1/animals/{animal_id}"
    animal_detail= requests.get(source_url, headers=headers).json()
    if animal_detail['Type'] == 'Dog':
        dog_detail = animal_detail
        web = f"https://www.bideawee.org/adopt-pet/{dog_detail['Name'].lower()}/{dog_detail['Internal-ID']}"
        urls.append(web)
        names.append(dog_detail['Name']) 
        ages.append(str(dog_detail['Age'])+" Months")
        breeds.append(dog_detail['Breed'])
        description=dog_detail['Description']
        descriptions_clean = re.sub(r"<br\s*/?>", " ", description, flags=re.IGNORECASE).replace('\n', ' ').replace('\r', ' ').replace('  ', ' ')
        descriptions.append(descriptions_clean.strip())
        genders.append(dog_detail['Sex'])
        images.append(dog_detail['CoverPhoto'])
        sizes.append(dog_detail['Size'])
        adoption_urls.append(f'https://www.shelterluv.com/matchme/adopt/WEE-A-{dog_detail['ID']}')

print('Data collection complete. Starting to save to CSV...')

print(len(names), len(ages), len(genders), len(breeds), len(descriptions), len(images), len(sizes), len(adoption_urls), len(urls))

df = pd.DataFrame({
    'Name': names,
    'Age': ages,
    'Gender': genders,
    'Breed': breeds,
    'Description': descriptions,
    'Image_URL': images,
    'Adoption_URL': adoption_urls,
    'sizes': sizes,
    'urls': urls
})
df.to_csv("/Users/galaxyrailwaytoto/Desktop/final_project/normalization/bideawee.csv", index=False)

print('CSV file created successfully.')




