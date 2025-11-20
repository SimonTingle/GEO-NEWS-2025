import newspaper
import spacy
from geopy.geocoders import Nominatim
from collections import Counter

# 1. Load the Natural Language Processing Model
# 'en_core_web_sm' is the small English model. Use 'trf' or 'lg' for better accuracy in production.
nlp = spacy.load("en_core_web_sm")

# 2. Initialize the Geocoder (converts names to Lat/Lon)
# You must provide a unique user_agent to identify your app to OpenStreetMap
geolocator = Nominatim(user_agent="my_3d_news_globe_prototype")

def get_location_from_url(url):
    print(f"--- Processing: {url} ---")
    
    # --- STAGE A: SCRAPING ---
    try:
        article = newspaper.Article(url)
        article.download()
        article.parse()
        print(f"Title Found: {article.title}")
    except Exception as e:
        print(f"Error downloading article: {e}")
        return None

    # --- STAGE B: NLP (Location Extraction) ---
    doc = nlp(article.text)
    
    # We look for entities labeled 'GPE' (Geopolitical Entity)
    locations = [ent.text for ent in doc.ents if ent.label_ == 'GPE']
    
    if not locations:
        print("No locations found in text.")
        return None

    # Heuristic: The most frequently mentioned location is likely the focus.
    # In a real app, you might also check the first 50 characters (the "Dateline").
    most_common_loc = Counter(locations).most_common(1)[0][0]
    print(f"Target Location Identified: {most_common_loc}")

    # --- STAGE C: GEOCODING ---
    try:
        location_data = geolocator.geocode(most_common_loc)
        if location_data:
            coords = {
                "location_name": most_common_loc,
                "lat": location_data.latitude,
                "lon": location_data.longitude,
                "address": location_data.address
            }
            return coords
        else:
            print("Could not find coordinates for this location.")
            return None
    except Exception as e:
        print(f"Geocoding service error: {e}")
        return None

# --- TEST RUN ---
# We use a sample article URL (e.g., a BBC article about a specific place)
# You can change this URL to any news article you want to test.
test_url = "https://www.bbc.com/news/world-europe-68362802" # Example article
result = get_location_from_url(test_url)

if result:
    print("\nSUCCESS! Data for 3D Globe:")
    print(result)
else:
    print("\nFailed to extract data.")
