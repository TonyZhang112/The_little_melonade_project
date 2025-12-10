import requests
import pandas as pd

list_url = "https://mpr-public-api.uk.r.appspot.com/dogs"
detail_url = "https://mpr-public-api.uk.r.appspot.com/dog/"

names = []
ages = []
genders = []
breeds = []
descriptions = []
images = []
current_weights = []
energy_levels = []
adoption_urls = []
is_housebroken = []
urls = []

# 1. Get all adoptable dogs
dogs = requests.get(list_url).json()

print(f'Total dog profiles found: {len(dogs)}, start scraping details...')

for dog in dogs:
    dog_id = dog['Animal_ID']
    url = f"{detail_url}{dog_id}"
    web = f"https://www.muddypawsrescue.org/adoptable?dog={dog_id}"
    urls.append(web)
    dog_detail = requests.get(url).json()
    names.append(dog_detail['Name'])
    ages.append(dog_detail['Age'])
    genders.append(dog_detail['Sex'])
    breeds.append(dog_detail['Breed'])
    descriptions.append(dog_detail['Description'])
    images.append(dog_detail['CoverPhoto'])
    current_weights.append(dog_detail['CurrentWeightPounds'])
    energy_levels.append(dog_detail['Energy_Rating'])
    is_housebroken.append(dog_detail['Housebroken'])
    adoption_urls.append('https://muddypawsrescue.my.site.com/s/adoption-registration')

print('Data collection complete, saving to CSV...')

if len(names) == len(ages) == len(genders) == len(breeds) == len(descriptions) == len(images) == len(current_weights) == len(energy_levels) == len(is_housebroken) == len(adoption_urls):
    df = pd.DataFrame({
        'Name': names,
        'Age': ages,
        'Gender':   genders,
        'Breed': breeds,
        'Description': descriptions,
        'Image_URL': images,
        'Adoption_URL': adoption_urls,
        'current_weights': current_weights,
        'energy_levels': energy_levels,
        'Is_Housebroken': is_housebroken,
        'urls': urls
    })
    df.to_csv('/Users/galaxyrailwaytoto/Desktop/final_project/normalization/muddy_paws_dogs.csv', index=False)
    print('CSV file created successfully.')
else:
    print("Data length mismatch! Please check the data collected.")




