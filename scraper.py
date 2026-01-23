import requests
import json
import os

# 1. משיכת נתונים מ-API הממשלתי (עסקאות אחרונות)
def get_gov_data():
    # resource_id של מאגר עסקאות נדל"ן
    url = "https://data.gov.il/api/3/action/datastore_search?resource_id=d0eeed13-bba3-4ff2-9713-0aeb6df5b574&limit=50"
    try:
        response = requests.get(url)
        data = response.json()
        records = data['result']['records']
        return records
    except:
        return []

# 2. סריקת אתר נדל"ן קטן (דוגמה גנרית)
def scrape_small_site():
    # כאן בדרך כלל משתמשים ב-BeautifulSoup
    # לצורך הדוגמה, נחזיר נתונים מדומים שמדמים סריקה
    return [
        {"city": "חיפה", "price": 900000, "rooms": 3, "link": "https://example.com/1", "source": "לוח מקומי"},
        {"city": "באר שבע", "price": 750000, "rooms": 4, "link": "https://example.com/2", "source": "פייסבוק"}
    ]

# 3. לוגיקה למציאת "הזדמנויות"
def find_deals(gov_data, scraped_data):
    deals = []
    # חישוב מחיר ממוצע דמיוני (במציאות תצטרך לנתח את gov_data)
    avg_prices = {"חיפה": 1200000, "באר שבע": 950000}
    
    for item in scraped_data:
        city = item['city']
        if city in avg_prices:
            if item['price'] < avg_prices[city] * 0.8: # 20% מתחת לממוצע
                item['is_deal'] = True
                item['savings'] = avg_prices[city] - item['price']
                deals.append(item)
    return deals

if __name__ == "__main__":
    gov = get_gov_data()
    scraped = scrape_small_site()
    final_deals = find_deals(gov, scraped)
    
    # שמירה לקובץ JSON שהאתר יקרא
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(final_deals, f, ensure_ascii=False, indent=4)
