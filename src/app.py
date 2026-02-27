from shiny import App, ui, reactive
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

app_ui = ui.page_fillable(
    ui.panel_title("Title"),
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
        ui.layout_columns(
            ui.card("Card 1"),
            ui.card("Card 2"),
        ),
        ui.card("Card 3")
    ),
)


def server(input, output, session):
    @reactive.calc
    def df():
        clientele = input.clientele()
        br_list = [i + " Available" for i in input.br()]
        access_list = [i + " Available" for i in input.accessibility()]
        years = input.year()
        filtered_data = data[
            (data.Clientele == clientele) &
            (data[br_list] > 0).any(axis=1) &
            (data[access_list] > 0).any(axis=1) &
            (data['Occupancy Year'] >= years[0].year) &
            (data['Occupancy Year'] <= years[1].year)
        ]
        return filtered_data


app = App(app_ui, server=server)