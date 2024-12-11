# Straatwoordenboek.nl Scraper

This Python script scrapes Dutch street slang words from [Straatwoordenboek.nl](https://straatwoordenboek.nl) and saves them in a structured JSON format. The scraper processes each letter (A-Z), extracts word details, and organizes them alphabetically.

## Features
- **Extracts Details**:
  - Word
  - Meanings
  - Likes and Dislikes
  - Example Sentences (if available)
  - Creation Date
- **Skips Duplicates**: Avoids processing duplicate words.
- **Progress Tracking**: Displays real-time progress using `tqdm` for each letter, page, and word.
- **JSON Output**: Outputs the data in a clean and structured JSON format.

## Prerequisites
Install the required Python libraries:
```bash
pip install requests beautifulsoup4 tqdm
```

## How to Use
1.	Copy main.py to your project directory.
2. Run the script:
```bash
   python straatwoordenboek_scraper.py
```
## Output
The script produces a JSON file structured as follows:
```json
{
    "A": [
        {
            "word": "assie",
            "creation_date": 2008,
            "meanings": [
                {
                    "meaning": "hash",
                    "likes": 45,
                    "dislikes": 2,
                    "example": "ey macho heb je assie of wierie?"
                }
            ]
        }
    ],
    "B": [
        {
            "word": "brada",
            "creation_date": 2010,
            "meanings": [
                {
                    "meaning": "Broer",
                    "likes": 50,
                    "dislikes": 1,
                    "example": "Mijn brada is er altijd voor mij."
                }
            ]
        }
    ]
}
```

## Coming Features
- **Filter Similar Meanings**: Filter out similar meanings if they are simislar.
- **Meaning Categorization**: Categorize meanings into groups.