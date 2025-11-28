import feedparser
import newspaper
from newspaper import Config
import spacy
from geopy.geocoders import Nominatim
from collections import Counter
import json
from fake_useragent import UserAgent
import requests
import asyncio
import aiohttp
from aiohttp import ClientTimeout

# Initialize the UserAgent generator
ua = UserAgent()

# --- CONFIGURATION ---
config = Config()
config.browser_user_agent = ua.random
config.request_timeout = 10

print("⏳ Loading NLP model...")
nlp = spacy.load("en_core_web_sm")
geolocator = Nominatim(user_agent="news_geo_locator_rss_v2")

# ----------------------------------------------------------------------
# Fallback mapping for impossible or ambiguous geocodes
# ----------------------------------------------------------------------
fallback_locations = {
    "Gaza": "Gaza Strip",
    "Gaza City": "Gaza Strip",
    "Congo": "Democratic Republic of the Congo",
    "Georgia": "Georgia (country)",
    "Ivano": "Ivano-Frankivsk, Ukraine"
}

# ----------------------------------------------------------------------
# Context-aware scoring system
# ----------------------------------------------------------------------
def choose_best_location(doc, locations):
    bad_tokens = {
        "US", "U.S.", "USA", "America", "United States",
        "Truth Social", "Twitter", "X", "Meta", "Facebook", "Instagram"
    }

    filtered = [loc for loc in locations if loc not in bad_tokens]
    if not filtered:
        filtered = locations

    event_verbs = {
        "hit", "strike", "kill", "erupts", "attack", "explosion",
        "bomb", "flood", "earthquake", "erupted", "blasts", "shooting",
        "dies", "dead", "injured", "collapse", "crash"
    }

    scores = {}

    for ent in doc.ents:
        if ent.label_ != "GPE":
            continue

        name = ent.text
        score = 1

        if len(name.split()) > 1:
            score += 1

        window = doc[max(ent.start - 8, 0): min(ent.end + 8, len(doc))]
        for token in window:
            if token.lemma_.lower() in event_verbs:
                score += 4

        scores[name] = max(scores.get(name, 0), score)

    if not scores:
        return Counter(filtered).most_common(1)[0][0]

    return max(scores, key=scores.get)

# ----------------------------------------------------------------------
# Article parsing and debugging table
# ----------------------------------------------------------------------
def debug_gpe_table(scores):
    print("   🧪 GPE scoring table:")
    for k, v in scores.items():
        print(f"      {k}: {v}")

async def fetch_article_text(session, url):
    headers = {"User-Agent": ua.random}
    try:
        async with session.get(url, timeout=ClientTimeout(total=20), headers=headers) as resp:
            return await resp.text()
    except:
        return None

async def get_location_from_article_async(session, url):
    print(f"   reading: {url[:60]}...")

    html = await fetch_article_text(session, url)
    if not html:
        print("   ❌ ERROR: Could not fetch article HTML")
        return None

    article = newspaper.Article(url)
    try:
        article.set_html(html)
        article.parse()
    except Exception as e:
        print(f"   ❌ ERROR parsing article: {e}")
        return None

    doc = nlp(article.text)
    locations = [ent.text for ent in doc.ents if ent.label_ == "GPE"]

    if not locations:
        print("   ⚠️ No GPEs found")
        return None

    most_common = choose_best_location(doc, locations)

    # apply fallback
    if most_common in fallback_locations:
        most_common = fallback_locations[most_common]

    try:
        loc = geolocator.geocode(most_common)
        if not loc:
            print(f"   ❌ Geocode failed for {most_common}")
            return None

        return {
            "title": article.title,
            "location": most_common,
            "lat": loc.latitude,
            "lon": loc.longitude,
            "url": url
        }

    except:
        return None

# ----------------------------------------------------------------------
# Parallel async RSS + article fetch
# ----------------------------------------------------------------------
RSS_TIMEOUT = 15

rss_feeds = [
    "http://feeds.bbci.co.uk/news/world/rss.xml",
    "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    "https://www.aljazeera.com/xml/rss/all.xml",
    "https://www.reutersagency.com/feed/?best-topics=world&post_type=best",
    "https://apnews.com/rss",
    "https://www.theguardian.com/world/rss",
    "https://www.france24.com/en/rss",
    "https://www.dw.com/en/top-stories/world/s-1429/rss",
    "https://www.cbc.ca/cmlink/rss-world",
    "https://feeds.skynews.com/feeds/rss/world.xml",
    "https://www.nhk.or.jp/rss/news/cat0.xml",
    "https://www.latimes.com/world-nation/rss2.0.xml",
    # Additional 20 feeds (first batch)
    "https://www.washingtonpost.com/arcio/rss/category/world/",
    "https://www.independent.co.uk/news/world/rss",
    "https://www.scmp.com/rss/91/feed",
    "https://www.abc.net.au/news/feed/51120/rss.xml",
    "https://timesofindia.indiatimes.com/rssfeeds/296589292.cms",
    "https://www.thehindu.com/news/international/feeder/default.rss",
    "https://www.chinadaily.com.cn/rss/world_rss.xml",
    "https://english.elpais.com/rss/elpais/portada_america.xml",
    "https://www.jpost.com/rss/rssfeedsheadlines.aspx",
    "https://www.haaretz.com/cmlink/1.628737",
    "https://www.telegraph.co.uk/news/world/rss.xml",
    "https://www.politico.eu/feed/",
    "https://www.euronews.com/rss",
    "https://www.straitstimes.com/news/world/rss.xml",
    "https://www.dawn.com/feeds/world",
    "https://www.rt.com/rss/news/",
    "https://www.arabnews.com/rss.xml",
    "https://www.irishtimes.com/cmlink/news-1.1319192",
    "https://www.themoscowtimes.com/rss/news",
    "https://www.thelocal.com/feeds/news",
    # Additional 20 feeds (second batch)
    "https://www.channelnewsasia.com/api/v1/rss-outbound-feed?_format=xml",
    "https://www.koreatimes.co.kr/www/rss/news.xml",
    "https://www.japantimes.co.jp/feed/",
    "https://www.bangkokpost.com/rss/data/news.xml",
    "https://vnexpress.net/rss/news.rss",
    "https://www.nation.com.pk/rss/nation-news",
    "https://www.thenational.ae/rss.xml",
    "https://www.trtworld.com/feed/rss",
    "https://www.aa.com.tr/en/rss/default?cat=world",
    "https://www.iol.co.za/cmlink/1.730092",
    "https://mg.co.za/rss/",
    "https://www.news24.com/news24/southafrica/rss",
    "https://www.eluniversal.com.mx/rss.xml",
    "https://rss.clarin.com/rss/mundo/",
    "https://g1.globo.com/rss/g1/mundo/",
    "https://www.swissinfo.ch/eng/rss",
    "https://www.thestar.com/content/thestar/feed.world.rss2",
    "https://www.express.co.uk/posts/rss/78/world",
    "https://www.mirror.co.uk/news/world-news/?service=rss",
    "https://www.newsweek.com/rss",
    # Additional 20 feeds (third batch)
    "https://www.scotsman.com/news/world/rss",
    "https://www.standard.co.uk/rss",
    "https://www.ft.com/world?format=rss",
    "https://www.economist.com/the-world-this-week/rss.xml",
    "https://www.nzherald.co.nz/arc/outboundfeeds/rss/section/world/",
    "https://www.stuff.co.nz/rss/world",
    "https://www.smh.com.au/rss/world.xml",
    "https://www.theage.com.au/rss/world.xml",
    "https://www.xinhuanet.com/english/rss/worldrss.xml",
    "https://english.kyodonews.net/rss/news.xml",
    "https://en.yna.co.kr/RSS/news.xml",
    "https://www.malaymail.com/feed",
    "https://www.philstar.com/rss/headlines",
    "https://www.thejakartapost.com/news.rss",
    "https://www.thenews.com.pk/rss/1/1",
    "https://www.dailysabah.com/rssFeed/11",
    "https://www.hurriyetdailynews.com/feeds/homepage",
    "https://www.timesofisrael.com/feed/",
    "https://www.al-monitor.com/feed",
    "https://www.africanews.com/feed/"
]

async def process_feeds():
    final_data = []

    async with aiohttp.ClientSession() as session:
        for feed_url in rss_feeds:
            print(f"\n📡 Fetching RSS: {feed_url}")

            try:
                async with session.get(feed_url, timeout=ClientTimeout(total=RSS_TIMEOUT), headers={"User-Agent": ua.random}) as resp:
                    xml = await resp.text()
            except:
                print("   ❌ RSS fetch failed")
                continue

            feed = feedparser.parse(xml)

            tasks = []
            for entry in feed.entries[:2]:
                tasks.append(get_location_from_article_async(session, entry.link))

            results = await asyncio.gather(*tasks)
            for r in results:
                if r:
                    final_data.append(r)

    with open("news_data.json", "w") as f:
        json.dump(final_data, f, indent=4)

    print(f"\n🎉 Done! Saved {len(final_data)} locations to news_data.json")

if __name__ == "__main__":
    asyncio.run(process_feeds())
