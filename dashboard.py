import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc

# Read and prepare the data
file_path = "data/cicero-traffic-all-sources-med nyhetsbrev.xlsx"

# Skip first 2 rows and use row 3 as header (index 2)
df = pd.read_excel(file_path, sheet_name=0, skiprows=[0, 1])

# Rename columns to clean names
df.columns = ['Article', 'Total', 'Google', 'Facebook', 'Newsletter', 'ChatGPT',
              'LinkedIn', 'Pct_Google', 'Pct_Facebook', 'Pct_Newsletter',
              'Pct_ChatGPT', 'Pct_LinkedIn']

# Convert numeric columns
numeric_cols = ['Total', 'Google', 'Facebook', 'Newsletter', 'ChatGPT', 'LinkedIn',
                'Pct_Google', 'Pct_Facebook', 'Pct_Newsletter', 'Pct_ChatGPT', 'Pct_LinkedIn']

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Remove rows with missing Article names
df = df.dropna(subset=['Article'])

# Sort by Total traffic
df = df.sort_values('Total', ascending=False).reset_index(drop=True)

# Initialize the Dash app with Bootstrap theme
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define colors for sources
source_colors = {
    'Google': '#4285F4',
    'Facebook': '#1877F2',
    'Newsletter': '#FF6B6B',
    'ChatGPT': '#10A37F',
    'LinkedIn': '#0A66C2'
}

# App layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Cicero Traffic Dashboard", className="text-center mb-4 mt-4"),
            html.P("Analysis of traffic sources including Newsletter",
                   className="text-center text-muted mb-4")
        ])
    ]),

    # Filters
    dbc.Row([
        dbc.Col([
            html.Label("Number of Top Articles to Display:", className="fw-bold"),
            dcc.Slider(
                id='top-n-slider',
                min=5,
                max=50,
                step=5,
                value=20,
                marks={i: str(i) for i in range(5, 51, 5)},
                tooltip={"placement": "bottom", "always_visible": True}
            )
        ], width=6),
        dbc.Col([
            html.Label("Minimum Total Traffic:", className="fw-bold"),
            dcc.Slider(
                id='min-traffic-slider',
                min=0,
                max=2000,
                step=100,
                value=0,
                marks={i: str(i) for i in range(0, 2001, 400)},
                tooltip={"placement": "bottom", "always_visible": True}
            )
        ], width=6)
    ], className="mb-4"),

    # Summary cards
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(f"{len(df):,}", className="card-title text-primary"),
                    html.P("Total Articles", className="card-text")
                ])
            ])
        ], width=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(f"{df['Total'].sum():,}", className="card-title text-success"),
                    html.P("Total Traffic", className="card-text")
                ])
            ])
        ], width=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(f"{df['Google'].sum():,}", className="card-title",
                           style={'color': source_colors['Google']}),
                    html.P("Google Traffic", className="card-text")
                ])
            ])
        ], width=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(f"{df['Facebook'].sum():,}", className="card-title",
                           style={'color': source_colors['Facebook']}),
                    html.P("Facebook Traffic", className="card-text")
                ])
            ])
        ], width=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(f"{df['Newsletter'].sum():,}", className="card-title",
                           style={'color': source_colors['Newsletter']}),
                    html.P("Newsletter Traffic", className="card-text")
                ])
            ])
        ], width=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(f"{df['ChatGPT'].sum():,}", className="card-title",
                           style={'color': source_colors['ChatGPT']}),
                    html.P("ChatGPT Traffic", className="card-text")
                ])
            ])
        ], width=2)
    ], className="mb-4"),

    # Charts
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='traffic-sources-pie')
        ], width=6),
        dbc.Col([
            dcc.Graph(id='traffic-sources-bar')
        ], width=6)
    ], className="mb-4"),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='top-articles-bar')
        ], width=12)
    ], className="mb-4"),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='source-percentage-stacked')
        ], width=12)
    ], className="mb-4"),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='traffic-distribution-box')
        ], width=6),
        dbc.Col([
            dcc.Graph(id='source-scatter')
        ], width=6)
    ])

], fluid=True)

# Callbacks for interactivity
@callback(
    [Output('traffic-sources-pie', 'figure'),
     Output('traffic-sources-bar', 'figure'),
     Output('top-articles-bar', 'figure'),
     Output('source-percentage-stacked', 'figure'),
     Output('traffic-distribution-box', 'figure'),
     Output('source-scatter', 'figure')],
    [Input('top-n-slider', 'value'),
     Input('min-traffic-slider', 'value')]
)
def update_charts(top_n, min_traffic):
    # Filter data
    filtered_df = df[df['Total'] >= min_traffic].head(top_n)

    # 1. Pie chart - Overall traffic sources
    source_totals = {
        'Google': df['Google'].sum(),
        'Facebook': df['Facebook'].sum(),
        'Newsletter': df['Newsletter'].sum(),
        'ChatGPT': df['ChatGPT'].sum(),
        'LinkedIn': df['LinkedIn'].sum()
    }

    pie_fig = go.Figure(data=[go.Pie(
        labels=list(source_totals.keys()),
        values=list(source_totals.values()),
        marker=dict(colors=[source_colors[k] for k in source_totals.keys()]),
        hole=0.3
    )])
    pie_fig.update_layout(
        title="Overall Traffic Distribution by Source",
        height=400
    )

    # 2. Bar chart - Total traffic by source
    bar_fig = go.Figure(data=[
        go.Bar(
            x=list(source_totals.keys()),
            y=list(source_totals.values()),
            marker_color=[source_colors[k] for k in source_totals.keys()],
            text=list(source_totals.values()),
            texttemplate='%{text:,}',
            textposition='outside'
        )
    ])
    bar_fig.update_layout(
        title="Total Traffic by Source",
        xaxis_title="Source",
        yaxis_title="Traffic",
        height=400
    )

    # 3. Top articles by total traffic with source breakdown
    top_articles_fig = go.Figure()

    sources = ['Google', 'Facebook', 'Newsletter', 'ChatGPT', 'LinkedIn']
    for source in sources:
        top_articles_fig.add_trace(go.Bar(
            name=source,
            x=filtered_df['Article'],
            y=filtered_df[source],
            marker_color=source_colors[source]
        ))

    top_articles_fig.update_layout(
        title=f"Top {len(filtered_df)} Articles - Traffic by Source",
        xaxis_title="Article",
        yaxis_title="Traffic",
        barmode='stack',
        height=500,
        xaxis={'tickangle': -45},
        hovermode='x unified'
    )

    # 4. Stacked percentage chart
    stacked_fig = go.Figure()

    for source in sources:
        pct_col = f'Pct_{source}'
        stacked_fig.add_trace(go.Bar(
            name=source,
            x=filtered_df['Article'],
            y=filtered_df[pct_col],
            marker_color=source_colors[source]
        ))

    stacked_fig.update_layout(
        title=f"Traffic Source Distribution (%) - Top {len(filtered_df)} Articles",
        xaxis_title="Article",
        yaxis_title="Percentage (%)",
        barmode='stack',
        height=500,
        xaxis={'tickangle': -45},
        hovermode='x unified'
    )

    # 5. Box plot - Traffic distribution by source
    box_fig = go.Figure()

    for source in sources:
        box_fig.add_trace(go.Box(
            y=df[source],
            name=source,
            marker_color=source_colors[source]
        ))

    box_fig.update_layout(
        title="Traffic Distribution by Source (All Articles)",
        yaxis_title="Traffic",
        height=400
    )

    # 6. Scatter plot - Google vs Total traffic
    scatter_fig = px.scatter(
        filtered_df,
        x='Total',
        y='Google',
        size='Facebook',
        color='Newsletter',
        hover_data=['Article'],
        title=f"Google Traffic vs Total Traffic (Top {len(filtered_df)} Articles)",
        labels={'Total': 'Total Traffic', 'Google': 'Google Traffic'},
        color_continuous_scale='Reds'
    )
    scatter_fig.update_layout(height=400)

    return pie_fig, bar_fig, top_articles_fig, stacked_fig, box_fig, scatter_fig

if __name__ == '__main__':
    print("\n" + "="*80)
    print("🚀 Starting Cicero Traffic Dashboard...")
    print("="*80)
    print(f"\n📊 Loaded {len(df)} articles with traffic data")
    print(f"📈 Total traffic across all sources: {df['Total'].sum():,}")
    print("\n🌐 Dashboard will be available at: http://127.0.0.1:8050")
    print("\nPress CTRL+C to stop the server\n")
    print("="*80 + "\n")

    app.run(debug=True, host='0.0.0.0', port=8050)
