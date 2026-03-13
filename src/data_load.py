# Imports for data loading and wrangling
import pandas as pd

# Imports for AI Milestone 3
from pathlib import Path
from dotenv import load_dotenv
from chatlas import ChatAnthropic
import querychat


# Setting up the AI agent
# two .parent is for going back to repo root to find the .env for our SECRETS and API keys
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

chat_client = ChatAnthropic(
    model="claude-sonnet-4-0",
    system_prompt=(
        "You help users explore a Vancouver non-market housing dataset. "
        "Translate user questions into correct data queries. "
        "Use only the dataset columns that exist. "
        "Do not invent fields or values."
    ),
)

# Data wrangling
data = pd.read_csv("data/raw/non-market-housing.csv", sep=";")

data.rename(columns={"Clientele- Families": "Clientele - Families"}, inplace=True)
data = data.loc[data["Project Status"] == "Completed"]

data["Clientele"] = "Mixed"
data.loc[
    (data["Clientele - Seniors"] == 0) & (data["Clientele - Other"] == 0),
    "Clientele"
] = "Families"
data.loc[
    (data["Clientele - Families"] == 0) & (data["Clientele - Other"] == 0),
    "Clientele"
] = "Seniors"

room_types = ["1BR", "2BR", "3BR", "4BR", "Studio"]
for br in room_types:
    data[f"{br} Available"] = (data.filter(like=br).sum(axis=1) > 0).astype("int")

access_types = ["Accessible", "Adaptable", "Standard"]
for ac in access_types:
    data[f"{ac} Available"] = (data.filter(like=ac).sum(axis=1) > 0).astype("int")

data["Total Units"] = (
    data["Clientele - Families"] +
    data["Clientele - Seniors"] +
    data["Clientele - Other"]
)

# QUERYCHAT
# ai_data gives QueryChat a cleaner table to work with.
# It avoids geometry/extra columns that are less useful for natural-language querying.
ai_data = data[[
    "Index Number",
    "Name",
    "Address",
    "Operator",
    "Clientele",
    "Occupancy Year",
    "Total Units",
    "1BR Available",
    "2BR Available",
    "3BR Available",
    "4BR Available",
    "Studio Available",
    "Accessible Available",
    "Adaptable Available",
    "Standard Available"
]].copy()

qc = querychat.QueryChat(
    ai_data,
    "vancouver_non_market_housing",
    client=chat_client,
    greeting="""Hello! I'm here to help you explore and analyze the Vancouver non-market housing data. You can ask me to filter, sort, or answer questions about the dataset.

Here are some ideas to get started:

Explore the data
* Show me all housing units for seniors
* What is the average number of total units?

Filter and sort
* Filter to mixed clientele housing with 2BR available
* Sort the housing projects by occupancy year descending"""
)