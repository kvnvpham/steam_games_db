from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import pandas as pd
import os

DRIVER_PATH = os.environ.get("DRIVER_PATH")
STEAM_CHARTS_URL = "https://steamcharts.com/top"

driver = webdriver.Chrome(service=Service(DRIVER_PATH))
driver.get(STEAM_CHARTS_URL)

game_names = []
stats_link = []
current_players = []
for page in range(4):
    game_names += [name.text for name in driver.find_elements(By.CSS_SELECTOR, ".game-name a")]
    stats_link += [link.get_attribute('href') for link in driver.find_elements(By.CSS_SELECTOR, ".game-name a")]
    current_players += [num.text.replace(",", "") for num in driver.find_elements(By.CLASS_NAME, "num")]

    if page == 0:
        next_btn = driver.find_element(By.XPATH, "//*[@id='content-wrapper']/div[3]/div/a")
    else:
        next_btn = driver.find_element(By.XPATH, "//*[@id='content-wrapper']/div[3]/div/a[2]")
    next_btn.click()
    time.sleep(2)

num_players = [current_players[i] for i in range(0, len(current_players), 3)]
peak_players = [current_players[i] for i in range(1, len(current_players), 3)]
hours_played = [current_players[i] for i in range(2, len(current_players), 3)]

data = []
for i in range(len(game_names)):
    data.append(
        {
            "name": game_names[i],
            "stats": stats_link[i],
            "current_players": int(num_players[i]),
            "peak_players": int(peak_players[i]),
            "hours_played": int(hours_played[i])
        }
    )

game_table = pd.DataFrame(data)
game_table.to_csv("Top 100 Steam Games.csv")
