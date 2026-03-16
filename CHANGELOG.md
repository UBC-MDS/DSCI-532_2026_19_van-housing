# Changelog

## [0.4.0] - 2026-03-17

### Added

* App now reads from parquet via DuckDB ([#85](https://github.com/UBC-MDS/DSCI-532_2026_19_van-housing/pull/85))
* Advanced feature: selecting map points through drag box will display and update total buildings count and their summary ([#82](https://github.com/UBC-MDS/DSCI-532_2026_19_van-housing/pull/82))
* Added unit tests and playwright tests ([#91](https://github.com/UBC-MDS/DSCI-532_2026_19_van-housing/pull/91))

### Changed

Feedback addressed:

* Addressed map feedback (scroll, legend, zoom): ([#77](https://github.com/UBC-MDS/DSCI-532_2026_19_van-housing/pull/77)) via [#90](https://github.com/UBC-MDS/DSCI-532_2026_19_van-housing/pull/91)
* Addressed other UI feedback (scroll, wrong header, year decimal): ([#92](https://github.com/UBC-MDS/DSCI-532_2026_19_van-housing/pull/92)) via [#93](https://github.com/UBC-MDS/DSCI-532_2026_19_van-housing/pull/93)
* Addressed readme feedback (installation, license): ([#89](https://github.com/UBC-MDS/DSCI-532_2026_19_van-housing/pull/89)) via [#98](https://github.com/UBC-MDS/DSCI-532_2026_19_van-housing/pull/98)

### Fixed

* Fixed GIF not rendering: ([#99](https://github.com/UBC-MDS/DSCI-532_2026_19_van-housing/pull/99)) via [#100](https://github.com/UBC-MDS/DSCI-532_2026_19_van-housing/pull/100)

Feedback prioritization issue link: [#78](https://github.com/UBC-MDS/DSCI-532_2026_19_van-housing/pull/78)

### Known Issues

* Un-parsed code in the response of the AI agent chat ([#73](https://github.com/UBC-MDS/DSCI-532_2026_19_van-housing/issues/73))

### Release Highlight: [Box or Lasso Selection Tool for filtering]

**Description:**
A lasso/box selection tool is impletmented on the map. 
Users can now use the box selection tool to select an area as a filtering tool. 
The rest of the dashboard will also be filtered based on the selection of the lasso selection box

- **Option chosen:** D
- **PR:** [#82](https://github.com/UBC-MDS/DSCI-532_2026_19_van-housing/pull/82)
- **Why this option over the others:** The ability to select what you directly see on the map is an important features for map users. For example, you want to live near the Vancouver Harbour, you can see it, but you don't know what it is called. The tool now allows users to circle out the exact area they want to filter out, regardless of finding out the neighbourhood name.
- **Feature prioritization issue link:** [#61](https://github.com/UBC-MDS/DSCI-532_2026_19_van-housing/issues/61)

### Collaboration

Summary of workflow or collaboration improvements made since M3: we required at least one peer review before merging any PR and kept PRs scoped to one feature or fix with atomic, meaningful commits.

See CONTRIBUTING.md ([#96](https://github.com/UBC-MDS/DSCI-532_2026_19_van-housing/issues/96)) for M3 retrospective and M4 norms.

### Reflection

The dashboard achieves its goals of allowing users to filter the data according to what they are looking for, getting a sense of the supply, names, and locations of buildings of interest. In this milestone we also added a select box to filter by location. Additional features that could be added are: sorting of the dataframe and adding more attributes to the table.

Trade-offs: the feedback we prioritised were broken UI or documentation and those deprioritised were additional features - full rationale is in [#61](https://github.com/UBC-MDS/DSCI-532_2026_19_van-housing/issues/61) and ### Changed above.

The lectures in W4 on databases and tests were helpful for our work this milestone, along with an earlier lecture on advanced reactivity features.

Tests
* Unit tests for `get_filtered_data`:
    * `test_get_filtered_data`: Checks that data filtering works as expected in standard use case.
    * `test_get_filtered_data_filter_unspecified`: Checks that all relevant data is still selected when some filters are not specified.
    * `test_get_filtered_data_no_match`: Checks that an empty dataframe is returned when no data matches the filters.
* Playwright tests:
    * `test_initial_value_boxes`: Checks that total units card shows correct stats for the full dataset.
    * `test_dataframe_initial_structure`: Checks that table has correct columns and rows for the full dataset.
    * `test_reset_button_restores_defaults`: Checks that selecting Families filter changes total units card and reset button deselects all clientele options.

## [0.3.0] - 2026-03-08

### Added

* Querychat AI chat interface and a dataframe output component to see the filtered dataframe ([#64](https://github.com/UBC-MDS/DSCI-532_2026_19_van-housing/pull/64))
* Download button in AI tab ([#66](https://github.com/UBC-MDS/DSCI-532_2026_19_van-housing/pull/66))
* Added AI panel components ([#69](https://github.com/UBC-MDS/DSCI-532_2026_19_van-housing/pull/69))

### Changed

* Changed clientele radio button to checkboxes to allow for select all and coloured map by clientele. ([#63](https://github.com/UBC-MDS/DSCI-532_2026_19_van-housing/pull/63))
* Updated component alignment of dashboard main ([#71](https://github.com/UBC-MDS/DSCI-532_2026_19_van-housing/pull/71))

## [0.2.0] - 2026-02-28

### Added

* Added input filters for clientele, number of bedrooms, accessibility and year slider. ([#42](https://github.com/UBC-MDS/DSCI-532_2026_19_van-housing/pull/42))
* Added card for total number of buildings. ([#45](https://github.com/UBC-MDS/DSCI-532_2026_19_van-housing/pull/45))
* Added table showing details of filtered buildings. ([#45](https://github.com/UBC-MDS/DSCI-532_2026_19_van-housing/pull/45))
* Added map showing location of filtered buildings. ([#46](https://github.com/UBC-MDS/DSCI-532_2026_19_van-housing/pull/46))
* Added colorful map, and reset button ([#50](https://github.com/UBC-MDS/DSCI-532_2026_19_van-housing/pull/50))
* Added demo ([#51](https://github.com/UBC-MDS/DSCI-532_2026_19_van-housing/pull/51))


### Changed

* Removed project status filter because home buyers will likely only be interested in completed buildings, so the table is pre-filtered.
* Removed operator filter because there are too many options and it is probably not as relevant to home buyers.
* Changed from building quantity by operator to table with details because home buyers would be interested in specific projects rather than aggregates.
* Changed from building occupancy over time to total number of buildings because home buyers would be interested in total supply rather than the trend over time.

### Reflection

We have implemented all job stories.

Our final layout is similar to our sketch. The difference is we removed a few filters and changed the charts to a card showing the total number of buildings and a table showing details of buildings. These are documented above.

