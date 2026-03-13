from shiny import reactive, render, ui
from shinywidgets import render_plotly

import os
import json
import numpy as np
import pandas as pd
import plotly.express as px

from datetime import date

from data_load import data, qc


# defining logic and reactivity
def server(input, output, session):
    qc_vals = qc.server()
    # chat = ui.Chat("housing_chat") #connects the server to the UI chat box

    # @chat.on_user_submit #runs everytime the user sends a message
    # async def handle_user_input(user_input: str):
    #     response = await chat_client.stream_async(user_input) #sends the prompt to Claude
    #     await chat.append_message_stream(response) #streams the response back to the app

    @output
    @render.text
    def ai_title():
        return qc_vals.title() or "AI-filtered housing dataset"

    @output
    @render.data_frame
    def ai_data_table():
        return render.DataGrid(qc_vals.df())

    @output
    @render.text
    def ai_total_units():
        df_ai = qc_vals.df()
        if df_ai is None or len(df_ai) == 0:
            return "0"
        return f"{int(df_ai['Total Units'].sum()):,}"

    @output
    @render.text
    def ai_avg_age():
        df_ai = qc_vals.df()
        if df_ai is None or len(df_ai) == 0:
            return "N/A"

        current_year = date.today().year
        avg_age = (current_year - df_ai["Occupancy Year"]).mean()

        return f"{avg_age:.1f} years"

    @reactive.calc
    def df():
        filtered_data = data.copy()

        if input.clientele():
            filtered_data = filtered_data[
                filtered_data.Clientele.isin(input.clientele())
            ]

        if input.br():
            br_list = [i + " Available" for i in input.br()]
            filtered_data = filtered_data[
                (filtered_data[br_list] > 0).any(axis=1)
            ]

        if input.accessible():
            access_list = [i + " Available" for i in input.accessible()]
            filtered_data = filtered_data[
                (filtered_data[access_list] > 0).any(axis=1)
            ]

        years = input.year()
        filtered_data = filtered_data[
            (filtered_data["Occupancy Year"] >= years[0].year) &
            (filtered_data["Occupancy Year"] <= years[1].year)
        ]

        return filtered_data

    @output
    @render.text
    def total_units_card():
        return f"{int(df()['Total Units'].sum()):,}"

    @output
    @render.table
    def building_table():
        return df()[[
            "Index Number",
            "Name",
            "Occupancy Year"
        ]].sort_values("Occupancy Year")

    @reactive.calc
    def df_points():
        """Extract lon/lat from GeoJSON Point stored in 'Geom'."""
        d = df().copy()

        def parse_point(s):
            try:
                obj = json.loads(s) if isinstance(s, str) else s
                if obj.get("type") != "Point":
                    return (np.nan, np.nan)
                lon, lat = obj.get("coordinates", [np.nan, np.nan])
                return (lon, lat)
            except Exception:
                return (np.nan, np.nan)

        coords = d["Geom"].apply(parse_point)
        d["lon"] = coords.apply(lambda x: x[0])
        d["lat"] = coords.apply(lambda x: x[1])
        return d.dropna(subset=["lon", "lat"])

    def _zoom_for_bounds(lon_min, lon_max, lat_min, lat_max):
        lon_range = max(1e-6, lon_max - lon_min)
        lat_range = max(1e-6, lat_max - lat_min)
        max_range = max(lon_range, lat_range)

        if max_range > 30:
            return 2
        if max_range > 15:
            return 3
        if max_range > 8:
            return 4
        if max_range > 4:
            return 5
        if max_range > 2:
            return 6
        if max_range > 1:
            return 7
        if max_range > 0.5:
            return 8
        if max_range > 0.25:
            return 9
        if max_range > 0.12:
            return 10
        if max_range > 0.06:
            return 11
        if max_range > 0.03:
            return 12
        return 13

    @render_plotly
    def map():
        d = df_points()

        # Vancouver fallback (if filters return 0 rows)
        default_center = {"lat": 49.2827, "lon": -123.1207}
        default_zoom = 10

        token = os.getenv("MAPBOX_TOKEN")

        if token:
            px.set_mapbox_access_token(token)
            map_style = "streets"
        else:
            map_style = "open-street-map"

        if len(d) == 0:
            fig = px.scatter_mapbox(
                pd.DataFrame({"lat": [default_center["lat"]], "lon": [default_center["lon"]]}),
                lat="lat",
                lon="lon",
                zoom=default_zoom,
                center=default_center,
            )
            fig.update_traces(marker={"size": 1, "opacity": 0.0}, hoverinfo="skip")
            fig.update_layout(
                mapbox_style=map_style,
                margin=dict(l=0, r=0, t=0, b=0),
                height=600
            )
            return fig

        lon_min, lon_max = d["lon"].min(), d["lon"].max()
        lat_min, lat_max = d["lat"].min(), d["lat"].max()
        center = {
            "lon": float((lon_min + lon_max) / 2),
            "lat": float((lat_min + lat_max) / 2)
        }
        zoom = _zoom_for_bounds(lon_min, lon_max, lat_min, lat_max)

        fig = px.scatter_mapbox(
            d,
            lat="lat",
            lon="lon",
            color="Clientele",
            hover_name="Name" if "Name" in d.columns else None,
            hover_data=[c for c in ["Address", "Occupancy Year", "Clientele", "Operator"] if c in d.columns],
            zoom=zoom,
            center=center,
        )
        fig.update_traces(marker={"size": 9, "opacity": 0.75})
        fig.update_layout(
            mapbox_style=map_style,
            margin=dict(l=0, r=0, t=0, b=0),
            autosize=True
        )
        return fig

    @reactive.effect
    @reactive.event(input.reset)
    def _():
        ui.update_checkbox_group(
            "clientele",
            selected=[]
        )

        ui.update_selectize(
            "br",
            selected=[]
        )

        ui.update_selectize(
            "accessible",
            selected=[]
        )

        ui.update_slider(
            "year",
            value=[date(1971, 1, 1), date(2025, 12, 31)]
        )

    @render.download(filename="filtered_data.csv")
    def download_data():
        yield ai_data_table.data_view().to_csv()