import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import json
import math
import time

base_url = "https://straatwoordenboek.nl/letter/"

letters = [chr(i) for i in range(ord('a'), ord('z') + 1)]

straatwoorden_data = []

# Scrape data for each letter
for letter in letters:
    print(f"Scraping words starting with letter: {letter.upper()}")

    response = requests.get(f"{base_url}{letter}")
    if response.status_code != 200:
        print(f"Failed to load page for letter {letter.upper()} (Status code: {response.status_code})")
        continue

    soup = BeautifulSoup(response.content, 'html.parser')
    total_words_text = soup.find("strong", class_="text-gray-400 text-sm")
    if total_words_text:
        total_words = int(total_words_text.text.split("van")[1].split("woorden")[0].strip())
        words_per_page = 60
        total_pages = math.ceil(total_words / words_per_page)
    else:
        total_words = 0
        total_pages = 0

    # Progress bar for words
    with tqdm(total=total_words, desc=f"{letter.upper()} Pages", unit="words") as word_bar:
        page = 1
        seen_words = set()

        while page <= total_pages:
            url = f"{base_url}{letter}?page={page}"
            response = requests.get(url)
            if response.status_code != 200:
                print(f"Failed to load page: {url} (Status code: {response.status_code})")
                break

            soup = BeautifulSoup(response.content, 'html.parser')
            word_links = soup.find_all("a", class_="text-indigo-700")
            if not word_links:
                break

            for word_link in word_links:
                word = word_link.text.strip()
                word_url = word_link["href"]

                if word in seen_words:
                    word_bar.update(1)
                    continue  # Skip duplicate words

                seen_words.add(word)
                word_response = requests.get(word_url)
                if word_response.status_code == 200:
                    word_soup = BeautifulSoup(word_response.content, 'html.parser')
                    meaning_divs = word_soup.find_all("div", class_="c-media-body")
                    if not meaning_divs:
                        word_bar.update(1)
                        continue  # Skip words with no meanings

                    word_details = {
                        "word": word,
                        "meanings": []
                    }

                    # Extract word likes and dislikes
                    word_likes_button = word_soup.find("button", {"wire:click": lambda x: x and "upvote" in x})
                    word_dislikes_button = word_soup.find("button", {"wire:click": lambda x: x and "downvote" in x})
                    word_details["likes"] = int(word_likes_button.find("span").text.strip()) if word_likes_button else 0
                    word_details["dislikes"] = int(word_dislikes_button.find("span").text.strip()) if word_dislikes_button else 0

                    # Extract creation date
                    creation_date_span = word_soup.find("span", string=lambda x: x and "Sinds:" in x)
                    if creation_date_span:
                        creation_date_text = creation_date_span.find_next("span").text.strip()
                        word_details["creation_date"] = int(creation_date_text) if creation_date_text.isdigit() else None

                    # Extract meanings
                    for meaning_div in meaning_divs:
                        try:
                            meaning = meaning_div.find("span", class_="text-xl font-bold").text.strip()
                            likes = int(meaning_div.find("button", {"wire:click": lambda x: x and "upvote" in x}).find("span").text.strip())
                            dislikes = int(meaning_div.find("button", {"wire:click": lambda x: x and "downvote" in x}).find("span").text.strip())
                            example_div = meaning_div.find("div", class_="text-gray-500 mt-6 text-base italic prose-x")
                            example = example_div.find("p").text.strip() if example_div else None

                            word_details["meanings"].append({
                                "meaning": meaning,
                                "likes": likes,
                                "dislikes": dislikes,
                                "example": example
                            })
                        except Exception as e:
                            continue

                    straatwoorden_data.append(word_details)

                word_bar.update(1)
                time.sleep(0.5)

            page += 1
            word_bar.set_description(f"{letter.upper()} Page {page}/{total_pages}")

# Save data to JSON
output_file = "straatwoordenboek.json"
with open(output_file, mode="w", encoding="utf-8") as file:
    json.dump(straatwoorden_data, file, ensure_ascii=False, indent=4)

print(f"Scraping complete. Data saved to {output_file}.")