from io import StringIO
from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
import numpy as np
from tqdm import tqdm
import time


def save_team_stats(year):
    # This List was obtained manually from the Basketball Reference website
    teams = [
        "BOS",
        "NYK",
        "PHI",
        "BRK",
        "TOR",
        "MIL",
        "CLE",
        "IND",
        "CHI",
        "DET",
        "ORL",
        "MIA",
        "ATL",
        "CHO",
        "WAS",
        "DEN",
        "UTA",
        "OKC",
        "POR",
        "MIN",
        "GSW",
        "LAC",
        "SAC",
        "LAL",
        "PHO",
        "HOU",
        "SAS",
        "DAL",
        "MEM",
        "NOP",
    ]
    
    # Loop through each team and save the HTML file
    for team in tqdm(teams, desc="Teams"):
        url = f"https://www.basketball-reference.com/teams/{team}/{year}/gamelog/"
        response = requests.get(url)

        try:
            if response.status_code == 200:
                with open(
                    f"Team Stats HTML/TS_{team}_{year}.html", "w", encoding="utf-8"
                ) as file:
                    file.write(response.text)
        except:
            print(f"Error: {team} {year}")

        # Sleep for 2 second to avoid being blocked
        time.sleep(2)

def main():
    year = 2023
    save_team_stats(year)

if __name__ == "__main__":
    main()


