
import pandas as pd
import os

BASICS_FILE = "title.basics.tsv.gz"
RATINGS_FILE = "title.ratings.tsv.gz"
OUTPUT_FILE = "imdb_top_movies.csv"

if not os.path.exists(BASICS_FILE):
    print("Missing file:", BASICS_FILE)
elif not os.path.exists(RATINGS_FILE):
    print("Missing file:", RATINGS_FILE)
else:
    print("Loading IMDb ratings dataset...")

    ratings = pd.read_csv(
        RATINGS_FILE,
        sep="\t",
        compression="gzip",
        na_values="\\N"
    )

    ratings = ratings[ratings["numVotes"] >= 25000]

    print("Loading movie details...")

    chunks = []

    for chunk in pd.read_csv(
    BASICS_FILE,
    sep="\t",
    compression="gzip",
    na_values="\\N",
    chunksize=200000,
    low_memory=False
):
        movies = chunk[chunk["titleType"] == "movie"]

        merged = movies.merge(ratings, on="tconst", how="inner")

        if not merged.empty:
            chunks.append(merged)

        print("Processed a batch of movie details.")

    if chunks:
        result = pd.concat(chunks, ignore_index=True)

        result = result.sort_values(
            ["averageRating", "numVotes"],
            ascending=[False, False]
        ).head(250)

        result.insert(0, "Rank", range(1, len(result) + 1))

        result = result.rename(columns={
            "primaryTitle": "Movie Title",
            "startYear": "Release Year",
            "averageRating": "IMDb Rating",
            "numVotes": "Number of Votes"
        })

        result = result[
            ["Rank", "Movie Title", "Release Year",
             "IMDb Rating", "Number of Votes"]
        ]

        result.to_csv(OUTPUT_FILE, index=False)

        print("\nSuccess! CSV file created:", OUTPUT_FILE)
        print(result.head(10).to_string(index=False))
    else:
        print("No matching movie records found.")
