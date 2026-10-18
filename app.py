
from flask import Flask, render_template_string
import pandas as pd
import requests
import os
import time

app = Flask(__name__)

CSV_FILE = "imdb_top_movies.csv"
TMDB_API_KEY = "37ae03dcc63e6d6b5f0b47cd29393dde"
POSTER_BASE = "https://image.tmdb.org/t/p/w500"

def load_movies():
    if not os.path.exists(CSV_FILE):
        return []

    df = pd.read_csv(CSV_FILE).fillna("")
    movies = df.to_dict(orient="records")

    # Load posters for the first 30 movies to limit API requests.
    cache_file = "poster_cache.csv"
    poster_cache = {}

    if os.path.exists(cache_file):
        cached = pd.read_csv(cache_file).fillna("")
        for _, row in cached.iterrows():
            poster_cache[str(row["key"])] = str(row["poster"])

    if TMDB_API_KEY != "PASTE_YOUR_TMDB_API_KEY_HERE":
        for movie in movies[:30]:
            title = str(movie["Movie Title"])
            year = str(movie["Release Year"]).split(".")[0]
            key = title + "|" + year

            if key not in poster_cache:
                try:
                    params = {
                        "api_key": TMDB_API_KEY,
                        "query": title
                    }

                    if year.isdigit() and year != "0":
                        params["year"] = year

                    response = requests.get(
                        "https://api.themoviedb.org/3/search/movie",
                        params=params,
                        timeout=10
                    )
                    response.raise_for_status()
                    results = response.json().get("results", [])

                    poster = ""
                    if results and results[0].get("poster_path"):
                        poster = POSTER_BASE + results[0]["poster_path"]

                    poster_cache[key] = poster
                    time.sleep(0.1)

                except requests.RequestException as error:
                    print("Poster lookup failed for", title, error)
                    poster_cache[key] = ""

            movie["Poster"] = poster_cache.get(key, "")

        pd.DataFrame([
            {"key": key, "poster": value}
            for key, value in poster_cache.items()
        ]).to_csv(cache_file, index=False)
    else:
        print("Add your TMDB API key to display movie posters.")
        for movie in movies:
            movie["Poster"] = ""

    for movie in movies:
        try:
            movie["Rank"] = int(float(movie["Rank"]))
            movie["Release Year"] = int(float(movie["Release Year"]))
            movie["IMDb Rating"] = float(movie["IMDb Rating"])
            movie["Number of Votes"] = int(float(movie["Number of Votes"]))
        except (ValueError, TypeError):
            pass

    return movies


MOVIES = load_movies()

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>IMDb Movie Explorer</title>
<style>
* { box-sizing: border-box; }
body {
    margin: 0;
    background: #10131c;
    color: #f5f5f5;
    font-family: Arial, sans-serif;
}
header {
    padding: 24px 6%;
    background: #191e2b;
    border-bottom: 1px solid #303747;
}
.brand { color: #f5c518; font-size: 28px; font-weight: 800; }
.brand span { color: white; }
header p { color: #aeb6c7; margin-bottom: 0; }
main { padding: 30px 6%; }
.hero {
    padding: 34px;
    margin-bottom: 28px;
    border-radius: 18px;
    background: linear-gradient(120deg, #292d3c, #171b28 65%, #40351b);
}
.eyebrow {
    color: #f5c518;
    font-size: 12px;
    font-weight: bold;
    letter-spacing: 2px;
}
h1 { font-size: clamp(28px, 4vw, 44px); margin: 12px 0; }
.hero p { color: #bdc4d2; max-width: 600px; line-height: 1.6; }
.stats { display: flex; gap: 12px; flex-wrap: wrap; margin-top: 22px; }
.stat {
    background: #222838;
    border: 1px solid #363e50;
    padding: 14px 18px;
    border-radius: 12px;
    min-width: 130px;
}
.stat strong { color: #f5c518; font-size: 23px; display: block; }
.stat span { font-size: 12px; color: #b7bfce; }
.section-title {
    display: flex; justify-content: space-between;
    align-items: center; gap: 12px; flex-wrap: wrap;
    margin: 28px 0 18px;
}
.section-title h2 { margin: 0; }
.section-title span { color: #aeb6c7; font-size: 13px; }
#search {
    width: 100%; padding: 15px 18px; margin: 0 0 22px;
    border-radius: 12px; border: 1px solid #394153;
    background: #1b2130; color: white; font-size: 15px;
    outline: none;
}
#search:focus { border-color: #f5c518; }
.grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(165px, 1fr));
    gap: 22px;
}
.card {
    background: #1b2130; border: 1px solid #2c3445;
    border-radius: 14px; overflow: hidden;
    transition: transform .2s, border-color .2s;
}
.card:hover { transform: translateY(-5px); border-color: #f5c518; }
.poster {
    width: 100%; aspect-ratio: 2 / 3; object-fit: cover;
    display: block; background: #292f3e;
}
.no-poster {
    aspect-ratio: 2 / 3; display: flex; align-items: center;
    justify-content: center; text-align: center; padding: 12px;
    color: #f5c518; background: linear-gradient(145deg, #292f3e, #151925);
}
.details { padding: 13px; }
.rank { color: #f5c518; font-size: 12px; font-weight: bold; }
.title {
    margin: 7px 0; font-size: 15px; line-height: 1.4;
    min-height: 42px; overflow-wrap: anywhere;
}
.year { color: #aeb6c7; font-size: 13px; }
.rating { color: #f5c518; font-weight: bold; margin-top: 12px; }
.votes { color: #aeb6c7; font-size: 12px; margin-top: 6px; }
footer { margin-top: 32px; color: #919bad; font-size: 12px; line-height: 1.6; }
#empty { display: none; color: #c4cbd8; padding: 25px 0; }
@media(max-width: 480px) {
    main { padding: 20px 4%; }
    .hero { padding: 22px; }
    .grid { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }
}
</style>
</head>
<body>
<header>
    <div class="brand">IMDb <span>Movie Explorer</span></div>
    <p>Your place to discover highly rated movies</p>
</header>
<main>
    <section class="hero">
        <div class="eyebrow">YOUR MOVIE COLLECTION</div>
        <h1>Find your next favourite film.</h1>
        <p>Explore movie posters, ratings and audience votes in one place.</p>
        <div class="stats">
            <div class="stat"><strong>{{ movies|length }}</strong><span>Movies listed</span></div>
            <div class="stat"><strong>★</strong><span>Rating insights</span></div>
            <div class="stat"><strong>⌕</strong><span>Instant search</span></div>
        </div>
    </section>

    <div class="section-title">
        <h2>Top-rated collection</h2>
        <span>Sorted by rating and vote count</span>
    </div>

    <input id="search" placeholder="🔍  Search by movie title..." oninput="filterMovies()">

    <div class="grid" id="movieGrid">
        {% for m in movies[:30] %}
        <article class="card" data-title="{{ m['Movie Title']|lower }}">
            {% if m.get('Poster') %}
            <img class="poster" src="{{ m['Poster'] }}" alt="Poster for {{ m['Movie Title'] }}" loading="lazy"
                 onerror="this.style.display='none';this.nextElementSibling.style.display='flex'">
            <div class="no-poster" style="display:none">🎬<br>{{ m['Movie Title'] }}</div>
            {% else %}
            <div class="no-poster">🎬<br>{{ m['Movie Title'] }}</div>
            {% endif %}
            <div class="details">
                <div class="rank">#{{ m['Rank'] }}</div>
                <div class="title">{{ m['Movie Title'] }}</div>
                <div class="year">{{ m['Release Year'] }}</div>
                <div class="rating">★ {{ m['IMDb Rating'] }}</div>
                <div class="votes">{{ "{:,}".format(m['Number of Votes']) }} votes</div>
            </div>
        </article>
        {% endfor %}
    </div>
    <div id="empty">No movies match your search.</div>

    <footer>
        Ratings and votes are from IMDb's published datasets. Posters are provided by TMDB.
        This is an educational project and is not affiliated with IMDb or TMDB.
        The ranking is calculated from rating and vote count; it is not the official IMDb Top 250 ranking.
    </footer>
</main>
<script>
function filterMovies() {
    const q = document.getElementById('search').value.toLowerCase();
    let visible = 0;
    document.querySelectorAll('.card').forEach(card => {
        const show = card.dataset.title.includes(q);
        card.style.display = show ? '' : 'none';
        if (show) visible++;
    });
    document.getElementById('empty').style.display = visible ? 'none' : 'block';
}
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML, movies=MOVIES)

if __name__ == "__main__":
    app.run(debug=True)
