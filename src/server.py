from datetime import date
import json
import os

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from shiny import reactive, render, ui
from shinywidgets import render_plotly

from .data_load import get_filtered_data, qc, data_pipeline

# defining logic and reactivity
def server(input, output, session):
    qc_vals = qc.server()

    # stores the Index Numbers of map selected points
    map_selected_indices = reactive.value(None)

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
    
    @render.download(filename="filtered_data.csv")
    def download_data():
        yield qc_vals.df().to_csv(index=False)

    @reactive.calc
    def df():
        years = input.year()
        year_range = (years[0].year, years[1].year)

        return get_filtered_data(
            data_pipeline(),
            clientele=input.clientele(),
            br=input.br(),
            accessible=input.accessible(),
            year_range=year_range,
        )

    # map selection layer on top of sidebar filter
    @reactive.calc
    def df_map_selected():
        base = df()
        indices = map_selected_indices.get()
        if indices is None:
            return base
        if len(indices) == 0:
            return base.iloc[0:0]
        return base[base["Index Number"].isin(indices)]

    @output
    @render.text
    def total_units_card():
        return f"{int(df_map_selected()['Total Units'].sum()):,}"

    @output
    @render.table
    def building_table():
        return df_map_selected()[[
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
            calculated = 2
        elif max_range > 15:
            calculated = 3
        elif max_range > 8:
            calculated = 4
        elif max_range > 4:
            calculated = 5
        elif max_range > 2:
            calculated = 6
        elif max_range > 1:
            calculated = 7
        elif max_range > 0.5:
            calculated = 8
        elif max_range > 0.25:
            calculated = 9
        elif max_range > 0.12:
            calculated = 10
        elif max_range > 0.06:
            calculated = 11
        elif max_range > 0.03:
            calculated = 12
        else:
            calculated = 13

        return max(calculated, 11)

    @render_plotly
    def map():
        d = df_points().copy()

        default_center = {"lat": 49.2827, "lon": -123.1207}
        default_zoom = 11

        token = os.getenv("MAPBOX_TOKEN")

        if token:
            px.set_mapbox_access_token(token)
            map_style = "streets"
        else:
            map_style = "open-street-map"

        if len(d) == 0:
            fig = px.scatter_mapbox(
                pd.DataFrame({
                    "lat": [default_center["lat"]],
                    "lon": [default_center["lon"]],
                }),
                lat="lat",
                lon="lon",
                zoom=default_zoom,
                center=default_center,
            )
            fig.update_traces(marker={"size": 1, "opacity": 0.0}, hoverinfo="skip")
            fig.update_layout(
                mapbox_style=map_style,
                margin=dict(l=0, r=0, t=0, b=0),
                autosize=True,
            )
            return go.FigureWidget(fig.data, fig.layout)

        if "Clientele" in d.columns:
            d["Clientele"] = (
                d["Clientele"]
                .fillna("Unknown")
                .astype(str)
                .str.strip()
                .replace({"": "Unknown", "nan": "Unknown", "None": "Unknown"})
            )
        else:
            d["Clientele"] = "Unknown"

        lon_min, lon_max = d["lon"].min(), d["lon"].max()
        lat_min, lat_max = d["lat"].min(), d["lat"].max()
        center = {
            "lon": float((lon_min + lon_max) / 2),
            "lat": float((lat_min + lat_max) / 2),
        }
        zoom = _zoom_for_bounds(lon_min, lon_max, lat_min, lat_max)

        fig = px.scatter_mapbox(
            d,
            lat="lat",
            lon="lon",
            color="Clientele",
            hover_name="Name" if "Name" in d.columns else None,
            hover_data=[
                c for c in ["Address", "Occupancy Year", "Clientele", "Operator"]
                if c in d.columns
            ],
            zoom=zoom,
            center=center,
            custom_data=["Index Number"],
        )

        fig.update_traces(marker={"size": 9, "opacity": 0.75})

        fig.update_layout(
            mapbox_style=map_style,
            margin=dict(l=0, r=0, t=0, b=0),
            autosize=True,
            dragmode="select",
            legend=dict(
                title_text="Clientele",
                x=0.01,
                y=0.99,
                xanchor="left",
                yanchor="top",
                bgcolor="rgba(255,255,255,0.8)",
                bordercolor="rgba(0,0,0,0.1)",
                borderwidth=1,
            ),
        )

        w = go.FigureWidget(fig.data, fig.layout)

        def on_selection(trace, points, selector):
            if points.point_inds:
                selected = [
                    trace.customdata[i][0]
                    for i in points.point_inds
                    if i < len(trace.customdata)
                ]
                map_selected_indices.set(selected if selected else None)
            else:
                map_selected_indices.set(None)

        def on_deselect(trace, points, selector):
            map_selected_indices.set(None)

        for trace in w.data:
            trace.on_selection(on_selection)
            trace.on_deselect(on_deselect)

        return w

    @reactive.effect
    @reactive.event(input.reset)
    def _():
        map_selected_indices.set(None)

        ui.update_checkbox_group("clientele", selected=[])
        ui.update_selectize("br", selected=[])
        ui.update_selectize("accessible", selected=[])
        ui.update_slider("year", value=[date(1971, 1, 1), date(2025, 12, 31)])
