# UBC-MDS-DSCI-532_2026_19_van-housing

## Vancouver Non-Market Housing Dashboard

This dashboard visualizes non-market housing in Vancouver using publicly available data from 2026. It is designed to help prospective homebuyers and renters understand the availability, types, and locations of non-market housing projects, while also supporting city planners in tracking development over time. Users can filter by neighborhood, housing type, and number of bedrooms, and view trends and proportions through interactive visualizations. The project highlights housing affordability issues and aims to provide actionable insights for both residents and policymakers.


## Team Members
- William Chong
- Claudia Liauw
- Jimmy Wang
- Sidharth Malik

## Development setup
To set up the development environment, clone the repository and create the conda environment using the provided `environment.yml` file:
```bash
git clone https://github.com/UBC-MDS/UBC-MDS-DSCI-532_2026_19_van-housing.git
cd UBC-MDS-DSCI-532_2026_19_van-housing
conda env create -f environment.yml
conda activate 532-gp19
```

## Run dashboard
To run dashboard locally, follow these commands:
```bash
cd src
shiny run app.py
```
