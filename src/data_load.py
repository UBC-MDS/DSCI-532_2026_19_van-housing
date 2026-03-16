# Imports for data loading and wrangling
from pathlib import Path

import duckdb
import pandas as pd

# Imports for AI Milestone 3
from dotenv import load_dotenv
from chatlas import ChatAnthropic
import querychat


# -----------------------------
# Paths
# -----------------------------
ROOT = Path(__file__).resolve().parent.parent
PARQUET_PATH = ROOT / "data" / "processed" / "non-market-housing.parquet"
ENV_PATH = ROOT / ".env"


# -----------------------------
# Setting up the AI agent
# -----------------------------
load_dotenv(ENV_PATH)

chat_client = ChatAnthropic(
    model="claude-sonnet-4-0",
    system_prompt=(
        "You help users explore a Vancouver non-market housing dataset. "
        "Translate user questions into correct data queries. "
        "Use only the dataset columns that exist. "
        "Do not invent fields or values."
    ),
)


# -----------------------------
# Read parquet using DuckDB
# -----------------------------
# Keep this simple and safe: DuckDB reads parquet, then we keep your existing
# wrangling logic almost unchanged.

def read_data_parquet(con):
    return con.execute(
        "SELECT * FROM read_parquet(?)",
        [str(PARQUET_PATH)],
    ).df()


# -----------------------------
# Data wrangling
# -----------------------------
def wrangle_data(data):
    if "Clientele- Families" in data.columns:
        data.rename(columns={"Clientele- Families": "Clientele - Families"}, inplace=True)

    # Keep only completed projects
    if "Project Status" in data.columns:
        data = data.loc[data["Project Status"] == "Completed"].copy()

    # Build Clientele label
    if all(
        col in data.columns
        for col in ["Clientele - Families", "Clientele - Seniors", "Clientele - Other"]
    ):
        data["Clientele"] = "Mixed"
        data.loc[
            (data["Clientele - Seniors"] == 0) & (data["Clientele - Other"] == 0),
            "Clientele",
        ] = "Families"
        data.loc[
            (data["Clientele - Families"] == 0) & (data["Clientele - Other"] == 0),
            "Clientele",
        ] = "Seniors"
    else:
        data["Clientele"] = "Mixed"

    # Bedroom availability flags
    room_types = ["1BR", "2BR", "3BR", "4BR", "Studio"]
    for br in room_types:
        matching_cols = [col for col in data.columns if br in col]
        if matching_cols:
            data[f"{br} Available"] = (data[matching_cols].sum(axis=1) > 0).astype(int)
        else:
            data[f"{br} Available"] = 0

    # Accessibility availability flags
    access_types = ["Accessible", "Adaptable", "Standard"]
    for ac in access_types:
        matching_cols = [col for col in data.columns if ac in col]
        if matching_cols:
            data[f"{ac} Available"] = (data[matching_cols].sum(axis=1) > 0).astype(int)
        else:
            data[f"{ac} Available"] = 0

    # Total units
    if all(
        col in data.columns
        for col in ["Clientele - Families", "Clientele - Seniors", "Clientele - Other"]
    ):
        data["Total Units"] = (
            data["Clientele - Families"].fillna(0)
            + data["Clientele - Seniors"].fillna(0)
            + data["Clientele - Other"].fillna(0)
        )
    else:
        data["Total Units"] = 0

    # Make sure Occupancy Year is numeric
    if "Occupancy Year" in data.columns:
        data["Occupancy Year"] = pd.to_numeric(data["Occupancy Year"], errors="coerce")
    
    return data


# -----------------------------
# Data pipeline
# -----------------------------
def data_pipeline() -> duckdb.DuckDBPyConnection:
    """Read in data from parquet, wrangle and register data. Return updated con."""
    con = duckdb.connect()

    data = read_data_parquet(con)

    data = wrangle_data(data)

    # Register the prepared table inside DuckDB.
    con.register("housing_prepared", data)

    return con


# -----------------------------
# Helper for filtered data
# -----------------------------
def _sql_list(values: list[str]) -> str:
    return ", ".join("'" + str(v).replace("'", "''") + "'" for v in values)

# def get_data() -> pd.DataFrame:
#     return con.execute("SELECT * FROM housing_prepared").df()


def get_filtered_data(
    con,
    clientele: list[str] | None = None,
    br: list[str] | None = None,
    accessible: list[str] | None = None,
    year_range: tuple[int, int] | None = None,
) -> pd.DataFrame:
    """Filter the prepared housing table in DuckDB, then return pandas output."""
    where_clauses = []

    if clientele:
        where_clauses.append(f'"Clientele" IN ({_sql_list(clientele)})')

    if br:
        br_clauses = [f'"{value} Available" = 1' for value in br]
        where_clauses.append("(" + " OR ".join(br_clauses) + ")")

    if accessible:
        access_clauses = [f'"{value} Available" = 1' for value in accessible]
        where_clauses.append("(" + " OR ".join(access_clauses) + ")")

    if year_range:
        start_year, end_year = year_range
        where_clauses.append(
            f'"Occupancy Year" BETWEEN {int(start_year)} AND {int(end_year)}'
        )

    query = "SELECT * FROM housing_prepared"
    if where_clauses:
        query += " WHERE " + " AND ".join(where_clauses)

    return con.execute(query).df()


# -----------------------------
# QUERYCHAT
# -----------------------------
con = duckdb.connect()
data = wrangle_data(read_data_parquet(con))
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
    "Standard Available",
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
* Sort the housing projects by occupancy year descending""",
)