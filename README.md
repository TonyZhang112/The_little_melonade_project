# The Little Melonade 🐶

**The Little Melonade** is a data-driven pet adoption recommendation system inspired by my rescue puppy, Melon.

## Project Description

Finding a rescue dog in NYC is a fragmented experience. Potential adopters often have to navigate dozens of shelter websites, each with different layouts, inconsistent data standards, and separate application processes. This friction often discourages potential adopters.

**The Little Melonade** solves this by building an end-to-end data pipeline:

1. **Data Collection:** Automated bots collect raw listings from major NYC shelters (Animal Haven, Muddy Paws, Pet Rescue, Wagtopia, Bideawee).
   1. Libraries used: request and bs4
2. **Data Engineering:** A robust normalization pipeline cleans, standardizes, and unifies inconsistent data (e.g., converting "82 months" to "Senior," or extracting numeric weights from unstructured text descriptions).
   1. library used: panda and regex
3. **Recommendation Engine:** An interactive CLI assistant ("Melon") interviews the user and uses a weighted scoring algorithm to find their perfect match based on lifestyle and dealbreakers.

The system currently aggregates and processes data for **400+ dogs** across 5 major data sources, while it is capable of processing more than 1000 dogs, I limited it to around 400 to save compute power.

## Rationale Statement

The inspiration comes from my rescue puppy, Melon, whom I adopted months ago from a NYC shelter. The motivation for this project stems from the difficulty and time-consuming process of searching for adoptable dogs across numerous shelters. When adopting a dog myself, the information felt scattered, requiring manual navigation through each individual website to find listings. This experience highlighted the need for a centralized resource that could simplify the process for others, so potential adopters are not discouraged by the tedious search. The project aims to create a more efficient and user-friendly way for people to explore shelter dogs and discover potential matches, ultimately helping more shelter dogs find homes. 

## Key Features

### 1. The Data Pipeline (`normalization.py`)

Raw data from shelters is notoriously messy. One shelter might list age as "2 months," another as "Puppy," and another as "0.2 Years."

- **Standardization:** Converts diverse Age, Size, and Energy formats into a unified schema.
- **Smart Extraction:** Uses Regex to extract data such as energy level and numeric weights from unstructured text descriptions to normalize data.
- **Data Imputation:** Handles missing values (e.g., "Unknown" energy levels) to ensure the matching engine functions without crashing.

### 2. The Recommendation Engine (`rec_sys.py`)

This is not a simple filter; it is a weighted scoring system designed to mimic a human adoption counselor.

- **Interactive Persona:** "Melon" acts as a chatbot assistant to gather user preferences naturally.
- **Intent Parsing:** Uses keyword matching (e.g., understanding that "I want a baby" means "Puppy").
- **Dealbreaker Logic:** Distinguishes between **Preferences** (which add bonus points to a score) and **Hard Requirements** (which disqualify a dog immediately).
- **Fairness Algorithm:** Includes specific logic for housebreaking. If a user says housebreaking is "not a strict requirement," the system ensures that non-housebroken dogs are not penalized in the ranking, giving "underdogs" a fair chance.

## Future Improvements

- **Web Interface:** Porting the CLI "Melon" assistant to a web app using Streamlit or React.
- **Real-Time Updates:** Setting up a cron job to run the scrapers daily and update the CSV automatically.
- **Image Recognition:** Using AI to auto-tag dog breeds or colors based on their profile photos.
- **User Input error handling:** Using LLM to analyze user input to better understand user preferences and allow a more natural conversational UI

## Files List

- `normalization.py`: The ETL script that merges raw CSVs, standardizes columns, and outputs the clean dataset.
- `rec_sys.py`: The interactive CLI tool that runs the matching algorithm.
- `all_dogs_normalized.csv`: The final, unified dataset used to power the recommendations.
- `scrapers/`: Folder containing individual scripts for Animal Haven, Muddy Paws, Wagtopia, etc.
