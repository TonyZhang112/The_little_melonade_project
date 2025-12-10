import pandas as pd
import numpy as np
import os
import webbrowser

def calculate_match_score(dog, user, hard_filter):
    score = 0
    
    # === Hard Filters ===
    
    # Housebroken
    if hard_filter.get('ishousebroken'):
        if dog['ishousebroken'] is not True:
            return 0
            
    # good with others
    if hard_filter.get('is_good_with_kids'):
        if dog['is_good_with_kids'] != 'True' and dog['is_good_with_kids'] is not True:
            return 0
            
    if hard_filter.get('is_good_with_dogs'):
        if dog['is_good_with_dogs'] != 'True' and dog['is_good_with_dogs'] is not True:
            return 0
            
    if hard_filter.get('is_good_with_cats'):
        if dog['is_good_with_cats'] != 'True' and dog['is_good_with_cats'] is not True:
            return 0

    # === SCORING  ===
    
    # 1. Age Match (+25 pts)
    if dog['age_group'] == user['age_group']:
        score += 25
        
    # 2. Size Match (+25 pts)
    if dog['size'] == user['size']:
        score += 25
        
    # 3. Energy Match (+15 pts)
    if dog['energy_level'] == user['energy_level']:
        score += 15
        
    # 4. Housebroken Bonus (+15 pts)
    if not hard_filter.get('ishousebroken'):
        if user['housebroken_pref']: 
            if dog['ishousebroken'] == True:
                score += 5
            
    # 5. Sex Match (+5 pts)
    if user.get('sex') != 'No Preference':
        if dog['sex'] == user['sex']:
            score += 5

    return score

def get_yes_no(prompt):
    while True:
        response = input(prompt + " (yes/no): ").strip().lower()
        if response in ['yes', 'y', 'yeah']:
            return True
        elif response in ['no', 'n', 'nope']:
            return False
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

def get_user_input():
    print ("\n\n-----------🐶Welcome to The Little Melonade🐶-----------\n\n"
           "--------A Pet Adoption Recommendation System--------\n\n"
           "----------------------------------------------------\n")
    print('I am Melon🐶, your personal pet adoption assistant! I will help you find the perfect furry friend!\n')

    user_profile = {}
    hard_filter = {}

    print ("First, I will ask you some questions get to know what kind of furry companion you are looking for!\n")

    age_pref = input("Do you want to bring a puppy, an adult or senior dog home? Or perhaps you have no Preference? ").strip().lower()
    if any(word in age_pref for word in ['baby', 'young', 'little', 'puppy']):
        user_profile['age_group'] = 'Puppy'
        print("\nGreat Choice! Who doesn't love a playful puppy full of energy?\n")
    elif any(word in age_pref for word in ['senior', 'old', 'elder']):
        user_profile['age_group'] = 'Senior'
        print("\nThank you so much for providing a home to them! Senior dogs are chill and always ready for some snuggles.\n")
    elif any(word in age_pref for word in ['adult', 'grown', 'mature']):
        user_profile['age_group'] = 'Adult'
        print("\nAdults are the perfect balance of energy and calmness. Great choice!\n")
    else:
        user_profile['age_group'] = 'no preference'
        print("\nNo preference noted. Love them all, Huh?\n")

    size_pref = input("What size of dog are you looking for? Small, Medium, Large, Extra Large or No Preference? ").strip().lower()
    if any(word in size_pref for word in ['small', 'tiny', 'little', 'mini']):
        user_profile['size'] = 'Small'
        print("\nSmall dogs are perfect for apartment living and are super cute!\n")
    elif any(word in size_pref for word in ['medium', 'mid', 'average']):
        user_profile['size'] = 'Medium'
        print("\nMedium-sized dogs are versatile and adapt well to various living situations!\n")
    elif any(word in size_pref for word in ['extra large', 'xl', 'extra big', 'giant']):
        user_profile['size'] = 'Extra Large'
        print("\nExtra Large dogs are gentle giants with big warm hearts!\n")
    elif any(word in size_pref for word in ['large', 'big']):
        user_profile['size'] = 'Large'
        print("\nLarge dogs are majestic and make great companions for active individuals!\n")
    else:
        user_profile['size'] = 'No Preference'
        print("\nNo size preference noted. Every dog is special!\n")

    sex_pref = input("Are you looking for a good boy or a good girl? Or sex doesn't really matter? ").strip().lower()
    if any(word in sex_pref for word in ['boy', 'male', 'he', 'him']):
        user_profile['sex'] = 'Male'
    elif any(word in sex_pref for word in ['girl', 'female', 'she', 'her']):
        user_profile['sex'] = 'Female'
    else:
        user_profile['sex'] = 'No Preference'
    if user_profile['sex'] == 'Male':
        print("\n Got it! A good boy it is!\n")
    elif user_profile['sex'] == 'Female':
        print("\n Got it! a good girl it is\n")
    else:
        print("\n No preference noted. All dogs are good dogs!\n")

    energy_level_pref = input("What energy level are you looking for in your pup? Low, Medium, High or No Preference? ").strip().lower()
    if any(word in energy_level_pref for word in ['low', 'chill', 'calm', 'relaxed']):
        user_profile['energy_level'] = 'Low'
        print("\nA calm and relaxed companion is a great choice for a peaceful home!\n")
    elif any(word in energy_level_pref for word in ['medium', 'moderate', 'balanced']):
        user_profile['energy_level'] = 'Medium'
        print("\nA balanced energy level is perfect for an active yet manageable lifestyle!\n")
    elif any(word in energy_level_pref for word in ['high', 'energetic', 'active', 'lively']):
        user_profile['energy_level'] = 'High'
        print("\nAn energetic companion will keep you on your toes and fill your life with excitement!\n")
    else:
        user_profile['energy_level'] = 'No Preference'
        print("\nNo preference noted. Every energy level has its own charm!\n")

    hb_hard = get_yes_no("Is having a housebroken dog the single most important thing for you (a strict requirement)?")
    if hb_hard:
        user_profile['housebroken_pref'] = True
        hard_filter['ishousebroken'] = True
        print("\n   Understood. We will strictly look for housebroken dogs.\n")
    else:
        hb_pref = input("Would you prefer a housebroken dog? ").strip().lower()
        if any(word in hb_pref for word in ['yes', 'y', 'yeah', 'yep']):
            user_profile['housebroken_pref'] = True
            hard_filter['ishousebroken'] = False
            print("\n   Great! We will prioritize housebroken dogs where possible.\n")
        else:
            user_profile['housebroken_pref'] = None
            hard_filter['ishousebroken'] = False
            print("\n   Thank YOU! Now every pups have fair chances, and can be house-trained!\n")

    is_other_around = get_yes_no("Do you have other pets or kids at home?")
    if is_other_around:
        good_with_kids = get_yes_no("Is it important that your new furry friend gets along well with kids?")
        good_with_dogs = get_yes_no("Is it important that your new furry friend gets along well with other dogs?")
        good_with_cats = get_yes_no("Is it important that your new furry friend gets along well with cats?")
        hard_filter['good_with_kids'] = good_with_kids
        hard_filter['good_with_dogs'] = good_with_dogs
        hard_filter['good_with_cats'] = good_with_cats
    else:
        hard_filter['good_with_kids'] = False
        hard_filter['good_with_dogs'] = False
        hard_filter['good_with_cats'] = False
    print(user_profile)
    return user_profile, hard_filter



def main():
    # 1. Load Data
    # Dynamically find the CSV file in the same folder as this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'all_dogs_normalized.csv')

    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: '{file_path}' not found. Please check the file name and location.")
        return

    # 2. Clean Boolean Column (Crucial Fix)
    # Pandas sometimes reads "True"/"False" strings as text. This forces them to be Real Booleans.
    df['ishousebroken'] = df['ishousebroken'].replace({
        'True': True, 'true': True, 
        'False': False, 'false': False
    })
    
    # 3. Get User Input
    user_prefs, user_filters = get_user_input()
    
    print("\n------------------------------------------------")
    print("Finding your perfect match...")

    # 4. Calculate Scores
    # We apply the 'Brain' (calculate_match_score) to every single row
    df['match_score'] = df.apply(
        lambda row: calculate_match_score(row, user_prefs, user_filters), 
        axis=1
    )
    
    # 5. Sort and Filter
    # Only keep dogs with a positive score (> 0)
    valid_matches = df[df['match_score'] > 0].copy()
    
    # Sort by highest score first
    valid_matches = valid_matches.sort_values(by='match_score', ascending=False)
    
    # 6. Display Results
    if valid_matches.empty:
        print("Oh no! No dogs matched your criteria. Try being more flexible with your dealbreakers!")
    else:
        print(f"\nWe found {len(valid_matches)} pawsome matches for you!\n")
        print("--- 🏆 TOP RECOMMENDATIONS 🏆 ---")
        
        # Loop through ALL valid matches (not just the top 5)
        for i, (_, dog) in enumerate(valid_matches.iterrows()):
            
            # 1. Print Dog Details
            print(f"\n--- Match #{i+1} ---") # Start count at 1
            
            # Handle pronouns
            if dog['sex'] == 'Male':
                pronoun = "he"
                possessive = "his"
            elif dog['sex'] == 'Female':
                pronoun = "she"
                possessive = "her"
            else:
                pronoun = "they"
                possessive = "their"

            print(f"Meet {dog['name']}! {pronoun.capitalize()} is a cute {str(dog['breed']).lower()} {str(dog['age_group']).lower()}.")
            
            words = str(dog['description']).split()
            short_desc = ' '.join(words[:40]) + "..."
            print(f"{short_desc}\n")
            
            see_photo = input(f"Do you want to see {possessive} photo? (y/n): ").strip().lower()
            if see_photo in ['y', 'yes']:
                print(f"Opening photo of {dog['name']} in your browser...")
                webbrowser.open(dog['image'])



            see_detail = input(f'Do you want to see {possessive} full description and adoption details here? (y/n): ').strip().lower()
            if see_detail in ['y', 'yes']:   
                webbrowser.open(dog['source_website'])
            
            print(f"You can apply to adopt {dog['name']} here: {dog['adoption_url']}\n")
            print("-" * 40)

            if i == len(valid_matches) - 1:
                print("That's all the matches we found! Thank you for using The Little Melonade!")
                break
            
            if (i + 1) % 5 == 0:
                print(f"\nYou have seen the top {i+1} matches.")
                choice = input("Do you want to see 5 more? (y/n): ").strip().lower()
                if choice not in ['y', 'yes']:
                    print("Thank you for using The Little Melonade! Wishing you the best!")
                    break
            else:
                choice = input("Do you want to see the next match? (y/n): ").strip().lower()
                if choice not in ['y', 'yes']:
                    print("Thank you for using The Little Melonade! Wishing you the best!")
                    break

if __name__ == "__main__":
    main()



