from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from app.services.webscapping import cheap_shark
import time


async def refresh_games():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--lang=pt-BR")
    options.add_experimental_option("prefs", {"intl.accept_languages": "pt-BR,pt"})
    options.add_argument(
        "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )

    navigator = webdriver.Chrome(options=options)
    navigator.set_window_size(1920, 1080)

    try:
        title_name_address = "//a[contains(@href, '/app/') and normalize-space(.) != '']"
        steam_url = "https://store.steampowered.com/charts/topselling/BR?l=portuguese"

        navigator.get(steam_url)
        time.sleep(3)

        top_games_preview = navigator.find_elements(By.XPATH, title_name_address)[:100]
        if top_games_preview:
            navigator.execute_script("arguments[0].scrollIntoView({block: 'center'})", top_games_preview[-1])
            time.sleep(2)

        top_games = navigator.find_elements(By.XPATH, title_name_address)[:100]
        top_games_titles = [game.text.strip() for game in top_games if game.text.strip()]
    finally:
        navigator.quit()

    return await cheap_shark.cheap_shark_search(top_games_titles)