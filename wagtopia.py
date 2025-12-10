import requests
import pandas as pd
import re
from bs4 import BeautifulSoup
import lxml


names = []
ages = []
genders = []
breeds = []
descriptions = []
images = []
adoption_urls = []
sizes = []
has_special_needs = []
is_housebroken = []
is_hypoallergenic = []
is_ok_with_other_cats = []
is_ok_with_other_dogs = []
is_ok_with_other_kids = []
is_spayed = []
weights = []
urls = []

headers = {
    "User-Agent": "Mozilla/5.0",
}
for i in (range(1,10)):
    url = f"https://petstablished.com/api/v2/public/search/?animal=Dog&zip=10001&geo_range=250&page={i}"
    dog_list = requests.get(url, headers=headers).json()['pets']
    for dog in dog_list:
        name = dog.get('pet_name')
        names.append(name)
        id = dog.get('pet_id')
        images.append(dog.get('results_photo_url'))
        url = f"https://petstablished.com/api/v2/public/search/pet/{id}"
        source_url = f"https://www.wagtopia.com/search/pet?id={id}"
        urls.append(source_url)
        dog_detail= requests.get(url).json()['pet']
        age = dog.get('age')
        ages.append(age)
        gender = dog_detail.get('sex')
        genders.append(gender)
        primary_breed = dog_detail.get('primary_breed')
        secondary_breed = dog_detail.get('secondary_breed')
        if secondary_breed:
            breed = f"{primary_breed}/{secondary_breed}"
        else:
            breed = primary_breed
        breeds.append(breed)
        description = dog_detail.get('description')
        if description:
            clean_desc = BeautifulSoup(description, "html.parser").get_text(separator=" ")
            clean_desc = " ".join(clean_desc.split()).strip()
        else:
            clean_desc = "N/A"
        descriptions.append(clean_desc)
        sizes.append(dog_detail.get('size'))
        has_special_needs.append(dog_detail.get('has_special_needs'))
        is_housebroken.append(dog_detail.get('is_housebroken'))
        is_hypoallergenic.append(dog_detail.get('is_hypoallergenic'))
        is_ok_with_other_cats.append(dog_detail.get('is_ok_with_other_cats'))
        is_ok_with_other_dogs.append(dog_detail.get('is_ok_with_other_dogs'))
        is_ok_with_other_kids.append(dog_detail.get('is_ok_with_other_kids'))
        is_spayed.append(dog_detail.get('is_spayed_neutered'))
        weights.append(dog_detail.get('weight'))
        adoption_urls.append(dog_detail.get('adopt_url'))


    print(f"Completed page {i}")


print(len(names))
print(len(ages))
print(len(genders))
print(len(breeds))
print(len(descriptions))
print(len(images))
print(len(adoption_urls))
print(len(sizes))
print(len(has_special_needs))
print(len(is_housebroken))
print(len(is_hypoallergenic))
print(len(is_ok_with_other_cats))
print(len(is_ok_with_other_dogs))
print(len(is_ok_with_other_kids))
print(len(is_spayed))
print(len(weights))

if len(names) == len(ages) == len(genders) == len(breeds) == len(descriptions) == len(images) == len(adoption_urls) == len(sizes) == len(has_special_needs) == len(is_housebroken) == len(is_hypoallergenic) == len(is_ok_with_other_cats) == len(is_ok_with_other_dogs) == len(is_ok_with_other_kids) == len(is_spayed) == len(weights) == len(urls):
    df = pd.DataFrame({
        'Name': names,
        'Age': ages,
        'Gender': genders,
        'Breed': breeds,
        'Description': descriptions,
        'Size': sizes,
        'Has_Special_Needs': has_special_needs,
        'Is_Housebroken': is_housebroken,
        'Is_Hypoallergenic': is_hypoallergenic,
        'Is_Ok_With_Other_Cats': is_ok_with_other_cats,
        'Is_Ok_With_Other_Dogs': is_ok_with_other_dogs,
        'Is_Ok_With_Other_Kids': is_ok_with_other_kids,
        'Is_Spayed_Neutered': is_spayed,
        'Weight': weights,
        'Image_URL': images,
        'Adoption_URL': adoption_urls,
        'urls': urls
    })
    df.to_csv('/Users/galaxyrailwaytoto/Desktop/final_project/normalization/wagtopia_dogs.csv', index=False)
else:
    print("Data length mismatch! Please check the data collected.")



