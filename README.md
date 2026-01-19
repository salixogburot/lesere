# Cicero Traffic Dashboard

An interactive web dashboard for analyzing website traffic sources from the Cicero dataset, including traffic from Google, Facebook, Newsletter, ChatGPT, and LinkedIn.

## Live Demo

**View the live dashboard:** [https://salixogburot.github.io/lesere/](https://salixogburot.github.io/lesere/)

The dashboard is available in two versions:
- **Static Web Version** (GitHub Pages): No installation required, works in any browser
- **Python Version** (Local): Full-featured Dash application for local development

## Features

- **Interactive Visualizations**: Multiple charts and graphs showing traffic patterns
- **Real-time Filtering**: Filter by number of top articles and minimum traffic threshold
- **Multiple Chart Types**:
  - Overall traffic distribution pie chart
  - Traffic totals by source (bar chart)
  - Top articles with source breakdown (stacked bar chart)
  - Source percentage distribution (stacked bar chart)
  - Traffic distribution analysis (box plots)
  - Correlation analysis (scatter plots)
- **Summary Statistics**: Quick overview cards showing key metrics
- **Responsive Design**: Built with Bootstrap for a clean, professional interface

## Data Overview

The dashboard analyzes traffic data from 523 articles with the following breakdown:

- **Total Traffic**: 35,980 views
- **Google**: 24,523 views (68.2%)
- **Newsletter**: 6,687 views (18.6%)
- **Facebook**: 3,113 views (8.7%)
- **LinkedIn**: 946 views (2.6%)
- **ChatGPT**: 711 views (2.0%)

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Setup

1. Clone the repository and navigate to the project directory:
```bash
cd /path/to/lesere
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

Or install packages individually:
```bash
pip install pandas openpyxl plotly dash dash-bootstrap-components
```

## Usage

### Running the Dashboard

1. Make sure you're in the project directory where `dashboard.py` is located

2. Run the dashboard:
```bash
python3 dashboard.py
```

3. Open your web browser and navigate to:
```
http://localhost:8050
```

4. The dashboard will display with default settings showing the top 20 articles

5. Use the interactive controls:
   - **Top Articles Slider**: Adjust to show between 5-50 top articles
   - **Minimum Traffic Slider**: Filter articles by minimum traffic threshold (0-2000)

### Stopping the Dashboard

Press `CTRL+C` in the terminal where the dashboard is running

## Dashboard Components

### Summary Cards
Shows aggregate statistics:
- Total number of articles
- Total traffic across all sources
- Individual traffic totals for each source

### Overall Traffic Distribution
A donut chart showing the percentage breakdown of all traffic by source

### Total Traffic by Source
A bar chart displaying absolute traffic numbers for each source

### Top Articles - Traffic by Source
A stacked bar chart showing traffic breakdown by source for the top articles

### Traffic Source Distribution (%)
A stacked percentage bar chart showing relative traffic proportions for each article

### Traffic Distribution by Source
Box plots showing the statistical distribution of traffic for each source across all articles

### Google Traffic vs Total Traffic
A scatter plot analyzing the correlation between Google traffic and total traffic, with bubble size representing Facebook traffic and color representing Newsletter traffic

## File Structure

```
lesere/
├── dashboard.py                    # Main Dash application (Python)
├── test_dashboard.py              # Data validation script
├── analyze_data.py                # Data analysis utility
├── export_data.py                 # Export data to JSON for web version
├── requirements.txt               # Python dependencies
├── README.md                      # This file
├── docs/                          # GitHub Pages static site
│   ├── index.html                 # Static HTML dashboard
│   └── traffic_data.json          # Exported traffic data
└── data/
    └── cicero-traffic-all-sources-med nyhetsbrev.xlsx  # Source data
```

## Data Source

The dashboard uses data from `data/cicero-traffic-all-sources-med nyhetsbrev.xlsx`, which contains:
- Article names
- Total traffic per article
- Traffic breakdown by source (Google, Facebook, Newsletter, ChatGPT, LinkedIn)
- Percentage distribution for each source

## GitHub Pages Deployment

The static web version is automatically deployed to GitHub Pages from the `docs/` folder.

### Updating the Live Dashboard

To update the data on the live site:

1. Update the Excel file in `data/`
2. Run the export script:
```bash
python3 export_data.py
```
3. Commit and push the changes:
```bash
git add docs/traffic_data.json
git commit -m "Update traffic data"
git push
```

### Configuring GitHub Pages

If you need to set up GitHub Pages for the first time:

1. Go to your repository on GitHub
2. Click **Settings** > **Pages**
3. Under **Source**, select **Deploy from a branch**
4. Select **main** branch and **/docs** folder
5. Click **Save**

The dashboard will be available at: `https://[username].github.io/[repository-name]/`

## Customization

### Changing Colors
Edit the `source_colors` dictionary in `dashboard.py`:
```python
source_colors = {
    'Google': '#4285F4',
    'Facebook': '#1877F2',
    'Newsletter': '#FF6B6B',
    'ChatGPT': '#10A37F',
    'LinkedIn': '#0A66C2'
}
```

### Adjusting Default Settings
Modify the default slider values in the layout section:
```python
dcc.Slider(
    id='top-n-slider',
    min=5,
    max=50,
    step=5,
    value=20,  # Change default value here
    ...
)
```

### Adding New Visualizations
Add new graph components in the layout and corresponding callbacks to update them based on filter changes.

## Troubleshooting

### Dashboard won't start
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check that the data file exists at the correct path
- Verify Python version is 3.7 or higher: `python3 --version`

### Data not loading
- Run `python3 test_dashboard.py` to verify data can be read correctly
- Check that the Excel file is not open in another application
- Ensure the file path is correct in `dashboard.py`

### Port already in use
If port 8050 is already in use, modify the port in `dashboard.py`:
```python
app.run(debug=True, host='0.0.0.0', port=8051)  # Change port number
```

## License

This project is for internal use with Cicero traffic data analysis.

## Support

For issues or questions, please contact the development team or create an issue in the project repository.