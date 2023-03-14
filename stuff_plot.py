import requests
from datetime import date, timedelta
from bs4 import BeautifulSoup
import pandas as pd
import lxml
import os
from functools import reduce
from fuzzywuzzy import fuzz


def parse_array_from_fangraphs_html(start_date, end_date):
    """
    Take a HTML stats page from fangraphs and parse it out to a dataframe.
    """
    # parse input
    PITCHERS_URL = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=0&type=36&season=2021&month=1000&season1=2015&ind=0&team=&rost=&age=&filter=&players=0&startdate={}&enddate={}&page=1_2000".format(
        start_date, end_date
    )
    # request the data
    pitchers_html = requests.get(PITCHERS_URL).text
    soup = BeautifulSoup(pitchers_html, "lxml")
    table = soup.find("table", {"class": "rgMasterTable"})

    # get headers
    headers_html = table.find("thead").find_all("th")
    headers = []
    for header in headers_html:
        headers.append(header.text)

    # get rows
    rows = []
    rows_html = table.find("tbody").find_all("tr")
    for row in rows_html:
        row_data = []
        for cell in row.find_all("td"):
            row_data.append(cell.text)
        rows.append(row_data)

    return pd.DataFrame(rows, columns=headers)

def scrape(periods):
    counter = 0
    for sdate, enddate in periods:
        print(sdate, enddate)
        dataset.append(parse_array_from_fangraphs_html(sdate, enddate))
        dataset[counter].to_csv(f"{enddate}.csv")
        counter += 1

    for i in range(0, len(dataset)):
        dataset[i] = dataset[i][["Name", "IP", "Stuff+", "Location+", "Pitching+"]].copy()

    df_merged = reduce(
        lambda left, right: pd.merge(left, right, on=["Name"], how="outer"), dataset
    ).fillna(0)
    return df_merged

"""
period = [

    ("2022-04-04", "2022-04-10"),
    ("2022-04-11", "2022-04-17"),
    ("2022-04-18", "2022-04-24"),
    ("2022-04-25", "2022-05-01"),
    ("2022-05-02", "2022-05-08"),
    ("2022-05-09", "2022-05-15"),
    ("2022-05-16", "2022-05-22"),
    ("2022-05-23", "2022-05-29"),
    ("2022-05-30", "2022-06-05"),
    ("2022-06-06", "2022-06-12"),
    ("2022-06-13", "2022-06-19"),
    ("2022-06-20", "2022-06-26"),
    ("2022-06-27", "2022-07-03"),
    ("2022-07-04", "2022-07-10"),
    ("2022-07-11", "2022-07-17"),
    ("2022-07-18", "2022-07-24"),
    ("2022-07-25", "2022-07-31"),
    ("2022-08-01", "2022-08-07"),
    ("2022-08-08", "2022-08-14"),
    ("2022-08-15", "2022-08-21"),
    ("2022-08-22", "2022-08-28"),
    ("2022-08-29", "2022-09-04"),
    ("2022-09-05", "2022-09-11"),
    ("2022-09-12", "2022-09-18"),
    ("2022-09-19", "2022-09-25"),
    ("2022-09-26", "2022-10-02"),
]
"""

dataset = []
period = [("2022-01-01","2022-12-01")]



merged = scrape(period)
merged.fillna(0).to_csv("master.csv")


exect = True
player_name = ""
while exect:
    player_name = input('Enter player name - NAME LASTNAME: ')

    # Create an empty dataframe to store matching rows
    matching_df = pd.DataFrame(columns=merged.columns)

    # Loop through each row of the original dataframe
    for index, row in merged.iterrows():
        # Use the fuzzywuzzy library to compare the name variable to the value in column B
        # If the match score is above the threshold of 70, add the row to the matching dataframe
        if fuzz.token_sort_ratio(player_name, row["Name"]) > 75:
            matching_df = matching_df.append(row)
    if (len(matching_df)) == 0:
        print("There were no matches")
    else:
        for a in range(0, len(matching_df)):
            print(str(a+1) + "-" + str(matching_df['Name'].iloc[a]) + 
            ", " + str(matching_df['IP'].iloc[a])  + 
            ", " + str(matching_df['Pitching+'].iloc[a])) 
        selection = int(input("Enter the number for your selection: "))
        matching_df = matching_df.iloc[[selection-1]]
    
    print("Your selection: ")
    print(str(matching_df['Name'].iloc[0]) + 
            ", " + str(matching_df['IP'].iloc[0])  + 
            ", " + str(matching_df['Pitching+'].iloc[0]))
    print(" ")
    test = input("Do you want to change the player? (y/n)")
    if (test.lower() == "n"):
        exect = False

player_id = str(matching_df['Name'].iloc[0])



#answer = input("Do you want to plot? (y/N)")
