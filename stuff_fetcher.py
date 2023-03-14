import requests
from datetime import date, timedelta
from bs4 import BeautifulSoup
import pandas as pd
import lxml
import os
from functools import reduce


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


periods = [
    ("2022-03-01", "2022-05-31"),
    ("2022-06-01", "2022-07-31"),
    ("2022-08-01", "2022-10-31"),
]

dataset = []
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

df_merged.to_csv("merged.csv")

