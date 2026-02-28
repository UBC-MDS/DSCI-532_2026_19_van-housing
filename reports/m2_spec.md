# Milestone 2 – Dashboard Prototype Specification

## 1. Updated Job Stories

| # | Job Story | Status | Notes |
|---|-----------|--------|-------|
| 1 | When I explore housing, I want to filter by occupancy year so I can limit my search to new developments. | Implemented | Changed from understanding supply over time to filtering because home buyers would be interested in specific projects rather than trend |
| 2 | When I want to explore projects for a specific client type, I want to filter by clientele type so I can focus on relevant buildings. | Implemented | As per milestone 1 |
| 3 | When I want to explore filtered data geographically, I want to see building locations on a map so I can understand spatial distribution. | Implemented | As per milestone 1 |
| 4 | When I am exploring affordable housing projects, I want to filter by bedroom count and building type so I can focus on relevant developments. | Implemented | Added story that was planned but not written |
| 5 | When I select filters, I want to see a summary metric so I can quickly understand total matching buildings. | Implemented | Added to give a quick sense of total supply |
| 6 | When I explore filtered data, I want to see building-level details in a table so I can inspect specific projects. | Implemented | Changed from bar chart to table because home buyers would be interested in specific projects rather than aggregates |

---

## 2. Component Inventory

| ID | Type | Shiny Widget / Renderer | Depends On | Job Story |
|----|------|------------------------|------------|------------|
| year | Input | `ui.input_slider()` | — | #1 |
| clientele | Input | `ui.input_radio_buttons()` | — | #2 |
| br | Input | `ui.input_selectize()` | — | #4 |
| accessibility | Input | `ui.input_selectize()` | — | #4 |
| df | Reactive calc | `@reactive.calc` | `year`, `clientele`, `br`, `accessibility` | #1, #2, #3, #4, #5, #6 |
| total_units_card | Output | `ui.output_text()` | df | #5 |
| building_table | Output | `ui.output_table()` | df | #6 |
| map | Output | `@render.plotly()` | df | #3 |

**Notes:**

- `df` is the main reactive calculation that filters the dataset based on all selected inputs.  
- All outputs depend on `df`, ensuring efficient reactivity (one calculation triggers all relevant outputs).  

---

## 3. Reactivity Diagram

```mermaid
flowchart TD
  A[/br/] --> F{{df}}
  B[/accessibility/] --> F
  C[/year/] --> F
  D[/clientele/] --> F
  F --> V([total_units_card])
  F --> T([building_table])
  F --> M([map])
```

## 4. Calculation Details

### 4.1 `df`
- **Depends on:** 
  - `br`
  - `accessibility`
  - `year`
  - `clientele`
- **Performs:** 
  - Filters the dataset to include only rows matching the selected bedroom count, building design type, occupancy year range, and client type. 
- **Consumed by:** 
  - `total_units_card`
  - `building_table`
  - `map`

### 4.2 `total_units_card`
- **Depends on:** `df`  
- **Performs:** Counts the number of buildings in the filtered dataset.  
- **Displayed as:** KPI summary card showing “Total Buildings”.

### 4.3 `building_table`
- **Depends on:** `df`  
- **Performs:** Selects and formats columns: Building Index, Building Name, Occupancy Year.  
- **Displayed as:** Interactive table for building-level exploration.

### 4.4 `map`
- **Depends on:** `df`  
- **Performs:** Plots building locations on a map using latitude/longitude.  
- **Displayed as:** Interactive map showing spatial distribution of filtered buildings.