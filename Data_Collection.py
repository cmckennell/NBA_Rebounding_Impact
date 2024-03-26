import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout
from tqdm import tqdm
import time
import logging
import os

# Set up logging
logging.basicConfig(
    filename=os.path.join("Logs", "data_collection.log"),  # Log file name
    filemode="a",  # Append mode, so logs are added to the file
    level=logging.INFO,  # Logging level
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log message format
    datefmt="%Y-%m-%d %H:%M:%S",  # Date format
)


def fetch_data_with_retry(url, max_retries=5):
    retry_wait = 1  # start with a 1-second wait time before retrying
    for attempt in range(max_retries):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Check for HTTP errors
            logging.info(f"Successfully fetched data from {url}")
            return response  # Return the response if no errors

        except (HTTPError, ConnectionError, Timeout) as err:
            logging.warning(f"Error occurred: {err} - Retrying in {retry_wait} seconds")

        except Exception as err:
            logging.error(
                f"An unexpected error occurred: {err} - Retrying in {retry_wait} seconds"
            )

        time.sleep(retry_wait)
        retry_wait *= 2  # Exponentially increase the wait time for each retry

    # If all retries fail, raise an exception
    logging.error(f"Failed to fetch data from {url} after {max_retries} attempts")
    raise Exception(f"Failed to fetch data from {url} after {max_retries} attempts")


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

        try:
            response = fetch_data_with_retry(url)  # Fetch the data with retry logic
            if response:
                with open(
                    f"Team Stats HTML/TS_{team}_{year}.html", "w", encoding="utf-8"
                ) as file:
                    file.write(response.text)  # Save the response HTML to a file
                logging.info(f"Successfully saved data for {team} {year}")

        except Exception as err:
            logging.error(f"An error occurred: {err} - Skipping {team} for {year}")


def main():
    year = 2023
    save_team_stats(year)


if __name__ == "__main__":
    main()
