import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc

# === Load cleaned data ===
df = pd.read_csv("notebooks/cleaned_movies.csv")
df = df.sort_values(by="Rating/Score", ascending=False)

# Top movie per genre
top_per_genre = df.loc[df.groupby("Genre")["Rating/Score"].idxmax()].reset_index(drop=True)

# === Initialize Dash app with dark Bootstrap theme ===
app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
app.title = "🎬 Movie Ratings by Genre"

# === App Layout ===
app.layout = dbc.Container([
    html.H1("🎬 Top Movies by Genre (2025)", className="text-center text-white my-4"),

    dbc.Card([
        dbc.CardHeader(html.H5("Click a genre to view all movies in that category", className="text-light bg-dark mb-0")),
        dbc.CardBody([
            dcc.Graph(
                id='genre-bar-chart',
                figure=px.bar(
                    top_per_genre,
                    x="Genre",
                    y="Rating/Score",
                    color="Rating/Score",
                    hover_data=["Title"],
                    title="Top-Rated Movie in Each Genre",
                    color_continuous_scale="RdYlBu_r",
                    template="plotly_dark"
                ).update_layout(
                    xaxis_title="Genre",
                    yaxis_title="Score",
                    xaxis_tickangle=-45,
                    plot_bgcolor='black',
                    paper_bgcolor='black',
                    font=dict(color='white'),
                    title_x=0.5,
                    coloraxis_colorbar=dict(title="Score"),
                    hoverlabel=dict(
                        font=dict(color='white'),
                        bgcolor='black'
                    )
                )
            )
        ])
    ], className="mb-4 bg-dark text-light shadow-sm"),

    dbc.Card([
        dbc.CardHeader(html.H5("Movies in Selected Genre", className="text-light bg-dark mb-0")),
        dbc.CardBody([
            dcc.Graph(id="movies-by-genre")
        ])
    ], className="bg-dark text-light shadow-sm")
], fluid=True)

# === Callback to update genre chart ===
@app.callback(
    Output("movies-by-genre", "figure"),
    Input("genre-bar-chart", "clickData")
)
def update_genre_chart(clickData):
    if clickData:
        selected_genre = clickData["points"][0]["x"]
        genre_df = df[df["Genre"] == selected_genre].copy()

        fig = px.bar(
            genre_df,
            x="Title",
            y="Rating/Score",
            color="Rating/Score",
            title=f"All {selected_genre} Movies (Colored by Score)",
            color_continuous_scale="RdYlBu_r",
            template="plotly_dark",
            labels={"Rating/Score": "Score"}
        )
        fig.update_layout(
            xaxis_tickangle=-45,
            plot_bgcolor='black',
            paper_bgcolor='black',
            font=dict(color='white'),
            title_x=0.5,
            coloraxis_colorbar=dict(title="Score"),
            hoverlabel=dict(
                font=dict(color='white'),
                bgcolor='black'
            )
        )
        return fig

    return px.bar(
        title="Click a genre above to explore its movies",
        template="plotly_dark"
    ).update_layout(
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(color='white'),
        title_x=0.5,
        hoverlabel=dict(
            font=dict(color='white'),
            bgcolor='black'
        )
    )

# === Run app ===
if __name__ == "__main__":
    app.run(debug=True)
