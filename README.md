# NBA Game Outcome Analysis: The Impact of Rebounds
## Overview
This project analyzes how team rebounding performance affects winning games in the National Basketball Association (NBA). By examining detailed game statistics, this analysis seeks to uncover the relationship between team rebounds and game outcomes.

## Project Structure
The project is organized into several Python scripts, each handling a specific part of the analysis:

- Data_Collection.py: Collects game statistics from the Basketball Reference website for NBA teams and saves them as HTML files.
- Data_Cleaning.py: Processes the collected HTML files, extracting relevant data and transforming it into a clean, structured format suitable for analysis.

Additional scripts for Exploratory Data Analysis, Modeling, and Presentation will be developed in subsequent phases of the project.

## Getting Started
### Prerequisites
- Python 3.8 or higher
- Libraries: pandas, beautifulsoup4, requests, tqdm

You can install the necessary libraries using pip:
`pip install pandas beautifulsoup4 requests tqdm`

## Data Collection
Run Data_Collection.py to fetch and store HTML files containing team statistics. The script accesses the Basketball Reference website and saves the data for each team and season specified.

`python Data_Collection.py`

## Data Cleaning
After collecting the data, run Data_Cleaning.py to clean and prepare the data for analysis. This script parses the HTML files, extracts relevant data, and transforms it into a structured DataFrame.

`python Data_Cleaning.py`

## Usage
Data Collection: Modify Data_Collection.py to specify the year and teams for which you want to collect data.
Data Cleaning: Data_Cleaning.py will read the downloaded HTML files and produce a clean, consolidated Excel file with all the team stats.