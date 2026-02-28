from shiny import App, ui, reactive, render
import pandas as pd
from datetime import date

import os
import json
import numpy as np
import plotly.express as px
from shinywidgets import output_widget, render_plotly

data = pd.read_csv('data/raw/non-market-housing.csv', sep=';')

# Data wrangling
data.rename(columns={'Clientele- Families': 'Clientele - Families'}, inplace=True)
data = data.loc[data['Project Status'] == 'Completed']

data['Clientele'] = 'Mixed'
data.loc[(data['Clientele - Seniors'] == 0) & (data['Clientele - Other'] == 0), 'Clientele'] = 'Families'
data.loc[(data['Clientele - Families'] == 0) & (data['Clientele - Other'] == 0), 'Clientele'] = 'Seniors'

room_types = ['1BR', '2BR', '3BR', '4BR', 'Studio']
for br in room_types:
    data[f'{br} Available'] = (data.filter(like=br).sum(axis=1) > 0).astype('int')

access_types = ['Accessible', 'Adaptable', 'Standard']
for ac in access_types:
    data[f'{ac} Available'] = (data.filter(like=ac).sum(axis=1) > 0).astype('int')

data['Total Units'] = (
    data['Clientele - Families'] + 
    data['Clientele - Seniors'] + 
    data['Clientele - Other']
)

# defining layout
app_ui = ui.page_fillable(
    ui.tags.style("""
        #map, #map > div {
            height: 100% !important;
        }

        #map .js-plotly-plot,
        #map .plot-container,
        #map .svg-container {
            height: 100% !important;
        }
    """),
    ui.h2("Non-market Housing Dashboard for the City of Vancouver", style="text-align:center; font-weight:700; font-size: 60px"),
    ui.p("Below are the buildings that match your selections.", style="text-align:center; margin-top:-8px; font-size: 36px; color:#666;"),
    ui.page_sidebar(
        ui.sidebar(
            ui.input_radio_buttons(
                "clientele",
                "Clientele",
                ["Families", "Seniors", "Mixed"]
            ),
            ui.input_selectize(
                "br",
                "Bedrooms",
                ["1BR", "2BR", "3BR", "4BR"],
                multiple=True
            ),
            ui.input_selectize(
                "accessible",
                "Accessibility",
                ["Standard", "Adaptable", "Accessible"],
                multiple=True
            ),
            ui.input_slider(
                "year",
                "Year",
                min=date(1971, 1, 1), max=date(2025, 12, 31),
                value=[date(1971, 1, 1), date(2025, 12, 31)],
                time_format='%Y'
            )
        ),
        ui.div(
            ui.layout_columns(
                # Total Units Card
                ui.card(
                    ui.h4("Total Buildings Count", style="color: #ffffff; text-align: center; font-weight: 500;"),
                    ui.div(
                        ui.output_text("total_units_card"),
                        style="""
                            font-size: 48px;
                            font-weight: bold;
                            text-align: center;
                            color: #ffffff;
                            text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
                        """
                    ),
                    style="""
                        background: linear-gradient(135deg, #6c5ce7, #a29bfe);
                        border-radius: 15px;
                        padding: 25px;
                        box-shadow: 0 6px 15px rgba(0,0,0,0.08);
                    """
                ),
                # Buildings Table Card
                ui.card(
                    ui.h4("Buildings Summary", style="text-align: center; font-weight: 500; color: #2d3436;"),
                    ui.div(
                        ui.output_table("building_table"),
                        style="""
                            width: 100%;
                            max-height: 350px;
                            overflow-y: auto;
                            background-color: #ffffff;
                            padding: 10px;
                        """
                    ),
                    style="""
                        border-radius: 15px;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
                        background-color: #ffffff;
                        border: 1px solid #dfe6e9;
                        display: flex;
                        flex-direction: column; 
                        align-items: center; 
                    """
                ),
                col_widths=[4, 8]
            ),
            ui.card(
                ui.h4("Map"),
                ui.div(
                    output_widget("map"),
                    style="height: 60vh;"
                ),
                style="""
                    margin-top: 20px;
                    flex-grow: 1;
                    display: flex;
                    flex-direction: column;
                """
            )
        )
    )
)


# defining logic and reactivity
def server(input, output, session):
    @reactive.calc
    def df():
        filtered_data = data.copy()
        filtered_data = filtered_data[
            filtered_data.Clientele == input.clientele()
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
            (filtered_data['Occupancy Year'] >= years[0].year) &
            (filtered_data['Occupancy Year'] <= years[1].year)
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

        if max_range > 30:  return 2
        if max_range > 15:  return 3
        if max_range > 8:   return 4
        if max_range > 4:   return 5
        if max_range > 2:   return 6
        if max_range > 1:   return 7
        if max_range > 0.5: return 8
        if max_range > 0.25:return 9
        if max_range > 0.12:return 10
        if max_range > 0.06:return 11
        if max_range > 0.03:return 12
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
            map_style = "light"
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
            fig.update_layout(mapbox_style="light", margin=dict(l=0, r=0, t=0, b=0), height=600)
            return fig

        lon_min, lon_max = d["lon"].min(), d["lon"].max()
        lat_min, lat_max = d["lat"].min(), d["lat"].max()
        center = {"lon": float((lon_min + lon_max) / 2), "lat": float((lat_min + lat_max) / 2)}
        zoom = _zoom_for_bounds(lon_min, lon_max, lat_min, lat_max)

        fig = px.scatter_mapbox(
            d,
            lat="lat",
            lon="lon",
            hover_name="Name" if "Name" in d.columns else None,
            hover_data=[c for c in ["Address", "Occupancy Year", "Clientele", "Operator"] if c in d.columns],
            zoom=zoom,
            center=center,
        )
        fig.update_traces(marker={"size": 9, "opacity": 0.75})
        fig.update_layout(mapbox_style="light", margin=dict(l=0, r=0, t=0, b=0), autosize=True)
        return fig
    

# For App Rendering, this line must be at the last
app = App(app_ui, server=server)