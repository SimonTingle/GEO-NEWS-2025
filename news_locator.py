import feedparser
import newspaper
from newspaper import Config
import spacy
from geopy.geocoders import Nominatim
from collections import Counter
import json
from fake_useragent import UserAgent

# Initialize the UserAgent generator
ua = UserAgent()

# --- CONFIGURATION ---
# FIX: Get a fresh, random browser User-Agent every time the script runs
config = Config()
config.browser_user_agent = ua.random
config.request_timeout = 10

# Load NLP & Geocoder
print("⏳ Loading NLP model...")
nlp = spacy.load("en_core_web_sm")
geolocator = Nominatim(user_agent="news_geo_locator_rss_v2")

def get_location_from_article(url):
    print(f"   reading: {url[:60]}...")
    
    # We must refresh the User-Agent before each download attempt
    article_config = Config()
    article_config.browser_user_agent = ua.random
    
    try:
        article = newspaper.Article(url, config=article_config)
        article.download()
        article.parse()
    except Exception as e:
        print(f"   ❌ ERROR: Download/Parse Failed: {e}")
        return None

    # NLP Extraction
    doc = nlp(article.text)
    locations = [ent.text for ent in doc.ents if ent.label_ == 'GPE']
    
    if not article.text:
        print(f"   ⚠️ FAIL: Article text content is empty.")
    
    if not locations:
        print(f"   ⚠️ FAIL: No GPEs (locations) found in text.")
        print(f"   (Text Length: {len(article.text)})")
        return None

    unique_locations = sorted(list(set(locations)))
    print(f"   🔍 GPEs found: {', '.join(unique_locations)}")
    
    most_common = Counter(locations).most_common(1)[0][0]
    
    # Geocode
    try:
        loc = geolocator.geocode(most_common)
        if loc:
            print(f"   ✅ FOUND: '{most_common}' -> ({loc.latitude}, {loc.longitude})")
            return {
                "title": article.title,
                "location": most_common,
                "lat": loc.latitude,
                "lon": loc.longitude,
                "url": url
            }
        else:
            print(f"   ❌ ERROR: Geocoder failed to find coordinates for '{most_common}'.")
    except Exception as e:
        print(f"   ❌ ERROR: Geocoding failed due to connection error.")
    
    return None

# --- MAIN EXECUTION ---
rss_feeds = [
    "http://feeds.bbci.co.uk/news/world/rss.xml",
    "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    "https://www.aljazeera.com/xml/rss/all.xml"
]

final_data = []
print(f"--- Processing {len(rss_feeds)} News Feeds ---")

for feed_url in rss_feeds:
    print(f"\n📡 Fetching RSS: {feed_url}")
    feed = feedparser.parse(feed_url)
    
    for entry in feed.entries[:2]:
        data = get_location_from_article(entry.link)
        if data:
            final_data.append(data)

# --- EXPORT ---
output_file = "news_data.json"
with open(output_file, "w") as f:
    json.dump(final_data, f, indent=4)

print(f"\n🎉 Done! Saved {len(final_data)} locations to {output_file}")
