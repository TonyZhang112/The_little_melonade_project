import pandas as pd
import re
import numpy as np

# Define our data sources
# Key = The name we want in the 'original_website' column
# Value = The actual filename on your disk

CSVs = {
    "Animal Haven": "/Users/galaxyrailwaytoto/Desktop/final_project/normalization/animal_heaven_dogs.csv",
    "Bideawee":     "/Users/galaxyrailwaytoto/Desktop/final_project/normalization/bideawee.csv",
    "Muddy Paws":   "/Users/galaxyrailwaytoto/Desktop/final_project/normalization/muddy_paws_dogs.csv",
    "Pet Rescue":   "/Users/galaxyrailwaytoto/Desktop/final_project/normalization/pet_rescue.csv",
    "Wagtopia":     "/Users/galaxyrailwaytoto/Desktop/final_project/normalization/wagtopia_dogs.csv"
}
# We will store our cleaned dataframes here
normalized_dfs = []

def normalize_age(age_val):
    age_cell = str(age_val).lower()
    
    # 1. Check for specific words first
    if 'puppy' in age_cell: return 'Puppy'
    if 'senior' in age_cell: return 'Senior'
    if 'adult' in age_cell: return 'Adult'
    
    # 2. Extract numbers
    years = 0
    # Check for "months" (e.g., "82 Months")
    month_match = re.search(r'(\d+\.?\d*)\s*month', age_cell)
    if month_match:
        years = float(month_match.group(1)) / 12
    else:
        # Check for "years" (e.g., "2.5 Years")
        year_match = re.search(r'(\d+\.?\d*)\s*year', age_cell)
        if year_match:
            years = float(year_match.group(1))
        elif 'year' in age_cell or 'yr' in age_cell: # e.g. "a year"
             years = 1
        else:
            return 'Adult' # Default fallback
            
    # 3. Apply Thresholds
    if years < 1: return 'Puppy'
    elif years <= 8: return 'Adult'
    else: return 'Senior'

def normalize_size(size_val, weight_val=None):
    if pd.notnull(size_val):
        s = str(size_val).lower() 
    else:
        s = ''
    if 'small' in s: return 'Small'
    if 'medium' in s: return 'Medium'
    if 'large' in s: return 'Large'
    if 'xl' in s or 'extra' in s: return 'Extra Large'
    if weight_val and pd.notnull(weight_val):
        try:
            w = float(weight_val)
            if w < 20: return 'Small'
            elif w <= 50: return 'Medium'
            elif w <= 90: return 'Large'
            else: return 'Extra Large'
        except:
            pass
    return 'Unknown'

def extract_weight(val):
    if pd.isnull(val): 
        return None
    s = str(val).lower()
    if '$' in s:
        # If it's a fee, try to find a number *after* the fee (e.g., "$325 56.0")
        match = re.search(r'\$?(\d+\.?\d+)', s)
        # If we found only one number, assume it's the fee and discard this entry
        if match and len(re.findall(r'\d+\.?\d+', s)) == 1:
            return None
    match = re.search(r'(\d+\.?\d+)', s)
    if match:
        return float(match.group(1)) 
    else:
        return None

def normalize_energy(level_val, desc_text=None):
    if pd.notnull(level_val):
        try:
            energy_level = float(level_val)
            if energy_level <= 2: return 'High'
            if energy_level == 3: return 'Medium'
            return 'Low'
        except: pass
    if desc_text and pd.notnull(desc_text):
        match = re.search(r'energy level.*?(\d+)', desc_text.lower())
        if match:
            v = int(match.group(1))
            # 10-point scale
            if v <= 3: return 'Low'
            elif v <= 6: return 'Medium'
            else: return 'High'
            
    return 'Unknown'

def check_housebroken(val, desc_text):
    if pd.notnull(val):
        s = str(val).lower() 
    else:
        s = ''
    if 'no' in s or 'false' in s: 
        return False
    elif 'yes' in s or 'true' in s: 
        return True
    if desc_text and pd.notnull(desc_text):
        if re.search(r'housebroken|potty trained|trained to go outside', desc_text.lower()):
            return True
        if re.search(r'not housebroken|not potty trained|needs training', desc_text.lower()):
            return False
    return None


for shelter_name, csv_path in CSVs.items():
    print(f"Processing {shelter_name}...")
    try:
        df = pd.read_csv(csv_path)
    except Exception as error:
        print(f"Could not load {shelter_name}: {error}")
        continue
    normalized = pd.DataFrame()
    normalized['name'] = df['Name'].astype(str).str.title()
    normalized['breed'] = df['Breed']
    normalized['sex'] = df['Gender']
    normalized['image'] = df['Image_URL']
    normalized['adoption_url'] = df['Adoption_URL']
    normalized['description'] = df['Description']
    normalized['age_group'] = df['Age'].apply(normalize_age)
    normalized['source_website'] = df['urls']
    if 'Is_Housebroken' not in df.columns:
        df['Is_Housebroken'] = None
    hb_col = df['Is_Housebroken']
    normalized['ishousebroken'] = [
        check_housebroken(hb_col[i] if hb_col is not None else None, desc) 
        for i, desc in enumerate(df['Description'])
    ]

    if shelter_name == "Animal Haven":
        normalized['current_weight'] = df['current_weights'].apply(extract_weight)
        normalized['size'] = df['Breed'].apply(normalize_size) 
        normalized['energy_level'] = 'Medium'
        normalized['is_good_with_kids'] = 'Unknown'
        normalized['is_good_with_dogs'] = 'Unknown'
        normalized['is_good_with_cats'] = 'Unknown'
    elif shelter_name == "Muddy Paws":
        normalized['current_weight'] = df['current_weights'].apply(extract_weight)
        normalized['size'] = normalized['current_weight'].apply(lambda w: normalize_size(None, w))
        normalized['energy_level'] = df['energy_levels'].apply(normalize_energy)
        normalized['is_good_with_kids'] = 'Unknown'
        normalized['is_good_with_dogs'] = 'Unknown'
        normalized['is_good_with_cats'] = 'Unknown'
    elif shelter_name == "Pet Rescue":
        normalized['current_weight'] = df['current_weights'].apply(extract_weight)
        normalized['size'] = df['sizes'].apply(normalize_size)
        normalized['energy_level'] = 'Medium'
        normalized['is_good_with_kids'] = 'Unknown'
        normalized['is_good_with_dogs'] = 'Unknown'
        normalized['is_good_with_cats'] = 'Unknown'
    elif shelter_name == "Wagtopia":
        normalized['current_weight'] = df['Weight'].apply(extract_weight)
        normalized['size'] = df['Size'].apply(normalize_size)
        normalized['energy_level'] = df['Description'].apply(lambda d: normalize_energy(None, d))
        normalized['is_good_with_kids'] = df['Is_Ok_With_Other_Kids']
        normalized['is_good_with_dogs'] = df['Is_Ok_With_Other_Dogs']
        normalized['is_good_with_cats'] = df['Is_Ok_With_Other_Cats']
    elif shelter_name == "Bideawee":
        normalized['current_weight'] = np.nan
        normalized['size'] = df['sizes'].apply(normalize_size)
        normalized['energy_level'] = 'Medium'
        normalized['is_good_with_kids'] = 'Unknown'
        normalized['is_good_with_dogs'] = 'Unknown'
        normalized['is_good_with_cats'] = 'Unknown'
    normalized_dfs.append(normalized)

print("Combining all normalized data...")

print(f"DataFrames to combine: {len(normalized_dfs)}")

final_df = pd.concat(normalized_dfs, ignore_index=True)

final_df.to_csv("/Users/galaxyrailwaytoto/Desktop/final_project/matching_sys/all_dogs_normalized.csv", index=False)

print("Done! File saved as 'all_dogs_normalized.csv'")
print(final_df.head())






