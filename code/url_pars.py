import requests
import urllib.parse
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9",
}

BASE = "https://www.epicurious.com"

def get_first_recipe_link(title):
    query = urllib.parse.quote_plus(title)
    url = f"https://www.epicurious.com/search?q={query}"

    try:
        resp = requests.get(url, headers=HEADERS, timeout=20)
        resp.raise_for_status()

        html = resp.text

        match = re.search(r'href="(/recipes/food/views/[^"]+)"', html)

        if match:
            return BASE + match.group(1)
        else:
            return "NaN"

    except Exception as e:
        print("Ошибка:", e)
        return "NaN"

def main():
    OUTPUT_FILE = "epi_links_last500.csv"
    df = pd.read_csv("data/epi_r_filtered.csv")

    last500 = df.tail(500)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("title,url\n")

    for title in last500["title"]:
        title = str(title).strip()
        print(f"Ищу рецепт: {title}")

        link = get_first_recipe_link(title)

        with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
            f.write(f'"{title}","{link}"\n')

        print(f"Ссылка: {link}")
        time.sleep(2)  
