import sys
sys.path.append('src')

import duckdb
import pandas as pd

from data_load import get_filtered_data


def make_toy_housing_data() -> pd.DataFrame:
    """Small in-memory dataset with all columns needed by get_filtered_data."""
    return pd.DataFrame(
        [
            {
                "Index Number": 1,
                "Name": "A",
                "Clientele": "Families",
                "Occupancy Year": 2010,
                "1BR Available": 1,
                "2BR Available": 1,
                "3BR Available": 0,
                "4BR Available": 0,
                "Studio Available": 0,
                "Accessible Available": 1,
                "Adaptable Available": 0,
                "Standard Available": 1,
            },
            {
                "Index Number": 2,
                "Name": "B",
                "Clientele": "Seniors",
                "Occupancy Year": 2018,
                "1BR Available": 1,
                "2BR Available": 0,
                "3BR Available": 0,
                "4BR Available": 0,
                "Studio Available": 1,
                "Accessible Available": 0,
                "Adaptable Available": 1,
                "Standard Available": 1,
            },
            {
                "Index Number": 3,
                "Name": "C",
                "Clientele": "Mixed",
                "Occupancy Year": 2022,
                "1BR Available": 0,
                "2BR Available": 1,
                "3BR Available": 1,
                "4BR Available": 0,
                "Studio Available": 0,
                "Accessible Available": 1,
                "Adaptable Available": 1,
                "Standard Available": 1,
            },
        ]
    )


def make_toy_connection() -> duckdb.DuckDBPyConnection:
    """Create a DuckDB connection with `housing_prepared` registered."""
    toy_con = duckdb.connect()
    toy_con.register("housing_prepared", make_toy_housing_data())
    return toy_con


def test_get_filtered_data() -> None:
    """Test expected use case."""
    toy_con = make_toy_connection()
    result = get_filtered_data(
        toy_con,
        clientele=["Families", "Mixed"],
        br=["2BR"],
        accessible=["Accessible"],
        year_range=(2010, 2025),
    )

    assert not result.empty
    assert set(result["Clientele"].unique()).issubset({"Families", "Mixed"})


def test_get_filtered_data_filter_unspecified() -> None:
    """Test that all data gets returned when filters not specified"""
    toy_con = make_toy_connection()
    result = get_filtered_data(
        toy_con,
        year_range=(2011, 2025),
    )

    assert not result.empty
    assert len(result) == 2


def test_get_filtered_data_no_match() -> None:
    """Test that an empty DataFrame is returned when no rows match the filters."""
    toy_con = make_toy_connection()
    result = get_filtered_data(
        toy_con,
        clientele=["Families"],
        year_range=(2020, 2025),
    )

    assert result.empty
