from shiny import ui
from datetime import date
from shinywidgets import output_widget

from data_load import qc


# defining layout
app_ui = ui.page_fillable(
    ui.tags.style("""
    body, html, .shiny-page {
        height: 100vh;
        overflow: hidden;
        margin: 0;
        padding: 0;
        font-family: 'Segoe UI', sans-serif;
        background-color: #f0f2f5;
    }

    #building_table table thead th {
        position: sticky;
        top: 0;
        z-index: 10;
        background: #dfe4ea;
        color: #2d3436;
        font-weight: 600;
        padding: 10px;
        text-align: center;
        border-bottom: 2px solid #b2bec3;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    #building_table table tbody td {
        padding: 10px;
        border-bottom: 1px solid #ecf0f1;
        text-align: center;
        color: #2d3436;
    }

    #building_table table tbody tr:nth-child(even) {
        background-color: rgba(255,255,255,0.15);
    }

    #building_table table tbody tr:hover {
        background-color: rgba(255,255,255,0.3);
    }

    /* Map styling */
    #map, #map > div {
        height: 100% !important;
    }

    #map .js-plotly-plot,
    #map .plot-container,
    #map .svg-container {
        height: 100% !important;
    }

        /* AI Explorer layout */
        .ai-explorer-page {
            height: calc(100vh - 140px);
            overflow: hidden;
        }

        .ai-explorer-page .bslib-sidebar-layout {
            height: 100%;
            overflow: hidden;
        }

        .ai-explorer-page .sidebar {
            height: 100%;
            overflow-y: auto;
        }

        .ai-results-col {
            height: 100%;
            min-height: 0;
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }

        .ai-results-col > .row,
        .ai-results-col .col,
        .ai-results-col .card {
            height: 100%;
            min-height: 0;
        }

        .ai-results-col .card {
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        .ai-results-col .card-body {
            flex: 1;
            min-height: 0;
            overflow-y: auto;
        }
    """),

    ui.h2(
        "Non-market Housing Dashboard for the City of Vancouver",
        style="text-align:center; font-weight:700; font-size: 40px"
    ),
    ui.p(
        "Below are the buildings that match your selections.",
        style="text-align:center; margin-top:-8px; font-size: 24px; color:#666;"
    ),

    ui.navset_tab(

        ui.nav_panel(
            "Dashboard",
            ui.page_sidebar(
                ui.sidebar(
                    ui.h4("Filters"),
                    ui.input_checkbox_group(
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
                        time_format="%Y"
                    ),
                    ui.input_action_button(
                        "reset",
                        "Reset Filters",
                        class_="btn btn-secondary",
                        style="margin-top: 15px; width: 100%;"
                    )
                ),

                ui.div(
                    ui.div(
                        ui.card(
                            ui.h4(
                                "Total Buildings Count",
                                style="color: #ffffff; text-align: center; font-weight: 500;"
                            ),
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
                                height: 200px;
                                box-shadow: 0 6px 15px rgba(0,0,0,0.08);
                            """
                        ),

                        ui.card(
                            ui.h4(
                                "Buildings Summary",
                                style="text-align: center; font-weight: 600; color: #ffffff;"
                            ),
                            ui.div(
                                ui.output_table("building_table"),
                                style="""
                                    width: 100%;
                                    max-height: 320px;
                                    overflow-y: auto;
                                    padding: 0;
                                    border-radius: 12px;
                                    background-color: transparent;
                                """
                            ),
                            style="""
                                border-radius: 15px;
                                box-shadow: 0 6px 15px rgba(0,0,0,0.08);
                                background: #777a7f;
                                border: 1px solid #dfe6e9;
                                display: flex;
                                flex-direction: column;
                                align-items: stretch;
                                flex-grow: 1;
                                padding: 12px;
                            """
                        ),

                        style="""
                            display:flex;
                            flex-direction:column;
                            gap:15px;
                            flex:4;
                            height:100%;
                        """
                    ),

                    ui.card(
                        ui.h4("Map"),
                        ui.div(
                            output_widget("map"),
                            style="flex-grow:1; height:100%;"
                        ),
                        style="""
                            display:flex;
                            flex-direction:column;
                            flex:8;
                        """
                    ),

                    style="""
                        display:flex;
                        flex-direction:row;
                        gap:20px;
                        height:700px;
                        align-items:stretch;
                    """
                )
            )
        ),

        ui.nav_panel(
            "AI Explorer",
            ui.div(
                ui.page_sidebar(
                    qc.sidebar(),
                    ui.div(
                        ui.card(
                            ui.card_header(ui.output_text("ai_title")),
                            ui.layout_columns(
                                ui.card(
                                    ui.h4(
                                        "Total Units",
                                        style="color:white; text-align:center;"
                                    ),
                                    ui.div(
                                        ui.output_text("ai_total_units"),
                                        style="""
                                            font-size:34px;
                                            font-weight:bold;
                                            text-align:center;
                                            color:white;
                                        """
                                    ),
                                    style="""
                                        background: linear-gradient(135deg, #00b894, #55efc4);
                                        border-radius:12px;
                                        padding:20px;
                                    """
                                ),

                                ui.card(
                                    ui.h4(
                                        "Average Building Age",
                                        style="color:white; text-align:center;"
                                    ),
                                    ui.div(
                                        ui.output_text("ai_avg_age"),
                                        style="""
                                            font-size:34px;
                                            font-weight:bold;
                                            text-align:center;
                                            color:white;
                                        """
                                    ),
                                    style="""
                                        background: linear-gradient(135deg, #0984e3, #74b9ff);
                                        border-radius:12px;
                                        padding:20px;
                                    """
                                ),
                                col_widths=[6, 6]
                            ),

                            ui.output_data_frame("ai_data_table"),

                            ui.download_button(
                                "download_data",
                                "Download Data",
                                class_="btn-primary"
                            ),

                            full_screen=True
                        ),
                        class_="ai-results-col"
                    )
                ),
                class_="ai-explorer-page"
            )
        )
    )
)