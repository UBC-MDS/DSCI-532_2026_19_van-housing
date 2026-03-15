from shiny import ui
from datetime import date
from shinywidgets import output_widget

from .data_load import qc


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

    #building_table,
    #building_table > *,
    #building_table > * > *,
    #building_table > * > * > *,
    #building_table > * > * > * > *,
    #building_table table,
    #building_table table tbody,
    #building_table table tbody tr {
        background: transparent !important;
    }

    #building_table table thead th {
        position: sticky;
        top: 0;
        z-index: 10;
        background: #00956e !important;
        color: #ffffff;
        font-size: 11px;
        font-weight: 700;
        padding: 8px 6px;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        border-bottom: 2px solid rgba(255,255,255,0.2);
    }

    #building_table table tbody td {
        padding: 8px 6px;
        font-size: 12px;
        text-align: center;
        color: #ffffff;
        border-bottom: 1px solid rgba(255,255,255,0.15);
    }

    #building_table table tbody tr:last-child td {
        border-bottom: none;
    }

    #building_table table tbody tr:nth-child(even) {
        background: rgba(255,255,255,0.1) !important;
    }

    #building_table table tbody tr:hover {
        background: rgba(255,255,255,0.2) !important;
    }


    /* Map styling */
    #map {
        height: 100% !important;
        overflow: hidden !important;
    }
    #map > div,
    #map .widget-subarea,
    #map .js-plotly-plot,
    #map .plot-container,
    #map .svg-container {
        height: 100% !important;
        overflow: hidden !important;
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

    .map-hint {
        font-size: 12px;
        color: #888;
        text-align: center;
        margin-top: 4px;
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

                        ui.div(
                            ui.h4(
                                "Buildings Summary",
                                style="text-align: center; font-weight: 700; color: #ffffff; letter-spacing: 0.01em; margin: 0 0 10px 0;"
                            ),
                            ui.div(
                                ui.output_table("building_table"),
                                style="""
                                    width: 100%;
                                    overflow-y: auto;
                                    overflow-x: hidden;
                                    padding: 0;
                                    border-radius: 12px;
                                    background: transparent !important;
                                    border: none !important;
                                    box-shadow: none !important;
                                    flex: 1 1 0;
                                    min-height: 0;
                                """
                            ),
                            style="""
                                border-radius: 15px;
                                background: linear-gradient(135deg, #00b894, #00896b);
                                box-shadow: 0 6px 20px rgba(0,184,148,0.25);
                                display: flex;
                                flex-direction: column;
                                flex: 1 1 0;
                                min-height: 0;
                                padding: 16px;
                                overflow: hidden;
                                box-sizing: border-box;
                            """
                        ),

                        style="""
                            display:flex;
                            flex-direction:column;
                            gap:15px;
                            flex:4;
                            height:100%;
                            min-height:0;
                        """
                    ),

                    ui.card(
                        ui.p(
                            "Tip: Use box-select or lasso (toolbar top-right) to filter by area.",
                            style="font-size:11px; color:#6c5ce7; margin:0 0 3px 0; padding:0; line-height:0.2; font-weight:500;"
                        ),
                        ui.div(
                            output_widget("map"),
                            style="""
                                flex: 1 1 0;
                                min-height: 0;
                                height: 0;
                                overflow: hidden;
                                margin: 0;
                                padding: 0;
                                border-radius: 10px;
                            """
                        ),
                        style="""
                            display: flex;
                            flex-direction: column;
                            flex: 8;
                            overflow: hidden;
                            padding: 8px 8px 0 8px;
                            margin: 0;
                            background: linear-gradient(160deg, #f8f6ff 0%, #eef9f6 100%);
                            border: 1.5px solid #d4ceff;
                            box-shadow: 0 6px 20px rgba(108,92,231,0.1);
                        """
                    ),

                    style="""
                        display:flex;
                        flex-direction:row;
                        gap:20px;
                        height:700px;
                        align-items:stretch;
                        box-sizing: border-box;
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
                                col_widths=[6,6]
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