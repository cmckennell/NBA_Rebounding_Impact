import pandas as pd
from io import StringIO
from bs4 import BeautifulSoup
import os
from tqdm import tqdm


def create_dataframe_from_html(file):
    # Load the HTML file with the correct encoding
    with open(file, "r", encoding="utf-8") as file:
        html_content = file.read()

    # Parse the HTML content
    soup = BeautifulSoup(html_content, "html.parser")
    tables = soup.find_all("table")

    # Convert the HTML table to a DataFrame
    df = pd.read_html(StringIO(str(tables)))[0]

    return df


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
    df_to_append = []
    for file in tqdm(os.listdir("Team Stats HTML")):
        # Create the file path
        file_path = os.path.join("Team Stats HTML", file)

        # Isolate the team name from the file name
        team = file.split("_")[1]

        # Create the DataFrame
        df = create_dataframe_from_html(file_path)

        #
        df = clean_data(df, team)
        df_to_append.append(df)

    # Concatenate the DataFrames
    df = pd.concat(df_to_append)

    # Save the DataFrame to an Excel file
    df.to_excel("Team Stats 2023.xlsx", index=False)


if __name__ == "__main__":
    main()
