import pandas as pd
from io import StringIO
from bs4 import BeautifulSoup
import os
from tqdm import tqdm
import logging

# Set up logging
logging.basicConfig(
    filename=os.path.join("Logs", "data_cleaning.log"),  # Log file name
    filemode="a",  # Append mode, so logs are added to the file
    level=logging.INFO,  # Logging level
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log message format
    datefmt="%Y-%m-%d %H:%M:%S",  # Date format
)


def create_dataframe_from_html(file):
    try:
        # Load the HTML file with the correct encoding
        with open(file, "r", encoding="utf-8") as file:
            html_content = file.read()

        # Parse the HTML content
        soup = BeautifulSoup(html_content, "html.parser")
        tables = soup.find_all("table")

        # Convert the HTML table to a DataFrame
        df = pd.read_html(StringIO(str(tables)))[0]
        logging.info(f"DataFrame created from {file}")
        return df
    except Exception as e:
        logging.error(f"Error creating DataFrame from {file}: {e}")
        return None


def clean_data(df, team):
    # Solve for the mutli-level column names
    new_columns = []
    for x in df.columns:
        if "Unnamed" not in x[0]:
            new_columns.append(f"{x[0]} {x[1]}")
        else:
            new_columns.append(f"{x[1]}")

    df.columns = pd.Index(new_columns)

    # Rename the location column
    df = df.rename(
        columns={
            "Unnamed: 3_level_1": "Game Location",
            "Tm": "Team Score",
            "Opp": "Opponent Score",
        }
    )

    # Solve for Duplicate Columns
    cols = df.columns.to_list()
    first_opponent_score_index = cols.index("Opponent Score")
    cols[first_opponent_score_index] = "Opponent"
    df.columns = cols

    # Drop the remaining empty columns
    for col in df.columns:
        if "Unnamed" in col:
            df = df.drop(columns=col)

    # Create a team column
    df["Team"] = team

    # Clean up the Game Location column
    df.loc[df["Game Location"] == "@", "Game Location"] = "Away"
    df.loc[df["Game Location"] != "Away", "Game Location"] = "Home"

    # Remove the rows with no data and the extra header rows from the HTML Table
    df = df.loc[((df["Date"] != "Date") & (df["Date"].notnull()))]

    # Reorder Columns
    col_order = [
        "Team",
        "Date",
        "Game Location",
        "W/L",
        "Team Score",
        "Opponent",
        "Opponent Score",
        "Team FG",
        "Team FGA",
        "Team FG%",
        "Team 3P",
        "Team 3PA",
        "Team 3P%",
        "Team FT",
        "Team FTA",
        "Team FT%",
        "Team ORB",
        "Team TRB",
        "Team AST",
        "Team STL",
        "Team BLK",
        "Team TOV",
        "Team PF",
        "Opponent FG",
        "Opponent FGA",
        "Opponent FG%",
        "Opponent 3P",
        "Opponent 3PA",
        "Opponent 3P%",
        "Opponent FT",
        "Opponent FTA",
        "Opponent FT%",
        "Opponent ORB",
        "Opponent TRB",
        "Opponent AST",
        "Opponent STL",
        "Opponent BLK",
        "Opponent TOV",
        "Opponent PF",
    ]
    df = df[col_order]

    # Reset the index
    df = df.reset_index(drop=True)

    return df


def main():
    # Loop Through the Team Stats HTML Files
    logging.info("Starting data cleaning process.")
    df_to_append = []
    team = 'Unknown Team'
    try:
        for file in tqdm(os.listdir("Team Stats HTML")):
            # Create the file path
            file_path = os.path.join("Team Stats HTML", file)

            # Isolate the team name from the file name
            team = file.split("_")[1]
            
            logging.info(f"Creating DataFrame from HTML for {team}.")
            
            df = create_dataframe_from_html(file_path) # Create the DataFrame   
            if df is not None:  
                df = clean_data(df, team) # Clean the data
                df_to_append.append(df) # Append the DataFrame to the list
                logging.info(f"Successfully cleaned data for {team}.")

    except Exception as e:
        logging.error(f"An error occurred: {e} for {team}.  Data not cleaned or appended.")
            
    
    try:
        df = pd.concat(df_to_append)
        df.to_excel("Team Stats 2023.xlsx", index=False)
        logging.info("Successfully saved the consolidated DataFrame to Excel.")

    except Exception as e:
        logging.error(f"Error saving DataFrame to Excel: {e}")

    logging.info("Data cleaning process completed.")


if __name__ == "__main__":
    main()
