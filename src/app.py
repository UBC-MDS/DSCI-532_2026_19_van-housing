from shiny import App, ui, reactive, render
import pandas as pd
from datetime import date

data = pd.read_csv('../data/raw/non-market-housing.csv', sep=';')

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

app_ui = ui.page_fillable(
    ui.panel_title("Van-housing"),
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
                    ui.h4("Total Units", style="color: #ffffff; text-align: center; font-weight: 500;"),
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
                    ui.h4("Buildings", style="text-align: center; font-weight: 500; color: #2d3436;"),
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
                    "Map will go here",
                    style="height: 400px; background-color: #e9ecef; display: flex; align-items: center; justify-content: center;"
                ),
                style="margin-top: 20px;"
            )
        )
    )
)


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
    


app = App(app_ui, server=server)