from shiny.playwright import controller
from shiny.run import ShinyAppProc
from shiny.pytest import create_app_fixture
from playwright.sync_api import Page

app = create_app_fixture("../src/app.py")


# test value box
def test_initial_value_boxes(page: Page, app: ShinyAppProc) -> None:
    """Total units card shows correct stats for the full dataset."""
    page.goto(app.url)
    page.wait_for_load_state("networkidle")

    controller.OutputText(page, "total_units_card").expect_value("28,950")


# test dataframe
def test_dataframe_initial_structure(page: Page, app: ShinyAppProc) -> None:
    """Summary dataframe has correct columns."""
    page.goto(app.url)
    page.wait_for_load_state("networkidle")

    data = controller.OutputTable(page, "building_table")
    data.expect_ncol(3)
    data.expect_column_labels(
        ["Index Number", "Name", "Occupancy Year"]
    )
    data.expect_nrow(551)


# test reset
def test_reset_button_restores_defaults(page: Page, app: ShinyAppProc) -> None:
    """Reset button returns all filters to their initial state."""
    page.goto(app.url)
    page.wait_for_load_state("networkidle")

    checkbox = controller.InputCheckboxGroup(page, "clientele")
    reset_btn = controller.InputActionButton(page, "reset")
    total_units = controller.OutputText(page, "total_units_card")

    # Change the filter, confirm it took effect
    checkbox.set(["Families"])
    total_units.expect_value("2,153")

    # Click reset and verify everything is restored
    reset_btn.click()
    total_units.expect_value("28,950")
    checkbox.expect_selected([])
