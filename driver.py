from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
import time
import csv

# Setup
chromedriver_autoinstaller.install()
options = Options()
options.headless = False
driver = webdriver.Chrome(options=options)

BASE_URL = "https://editorial.rottentomatoes.com/guide/best-new-movies/"
driver.get(BASE_URL)

WebDriverWait(driver, 15).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, "countdown-item"))
)

# Extract title + href + score from main page
movie_blocks = driver.find_elements(By.CLASS_NAME, "countdown-item")
movie_links = []

for block in movie_blocks:
    try:
        title_elem = block.find_element(By.CSS_SELECTOR, ".article_movie_title a")
        title = title_elem.text.strip()
        href = title_elem.get_attribute("href")
        score_elem = block.find_element(By.CSS_SELECTOR, ".tMeterScore")
        score = score_elem.text.strip()
        movie_links.append((title, href, score))
    except Exception as e:
        print(f"❌ Failed to extract from main page block: {e}")

movie_data = []

# Now visit each movie page to get genre
for title, href, score in movie_links:
    try:
        driver.get(href)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(1)

        # Genre from detail page
        try:
            genre_elements = driver.find_elements(By.XPATH, '//rt-text[@slot="metadataGenre"]')
            genre = [g.text.strip() for g in genre_elements]
        except:
            genre = ["Unknown"]

        print(f"✔ {title} — Genre: {genre} — Score: {score}")
        movie_data.append({
            "Title": title,
            "Genre": ", ".join(genre),
            "Rating/Score": score
        })

        # Go back to base page
        driver.get(BASE_URL)
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "countdown-item"))
        )
        time.sleep(1)

    except Exception as e:
        print(f"❌ Failed for {title}: {e}")

driver.quit()

# Save to CSV
with open("movies_with_genres.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["Title", "Genre", "Rating/Score"])
    writer.writeheader()
    writer.writerows(movie_data)

print("✅ Done and saved to movies_with_genres.csv")
